from collections import defaultdict
import matplotlib.pyplot as plt


def get_errors_and_correction(m2_in, processed_in, output, check=-40):
    errors = defaultdict(int)
    corrected = defaultdict(int)
    special_errors = []
    with open(m2_in, 'r',
              errors="ignore") as f_m2, open(processed_in,
                                             'r') as f_in, open(output,
                                                                'r') as f_out:
        f_m2, f_in, f_out = f_m2.readlines(), f_in.readlines(
        ), f_out.readlines()
        io_idx, m2_idx = 0, 0
        count = 0
        while io_idx < len(f_in) and m2_idx < len(f_m2):
            # print(count)
            i, o = f_in[io_idx], f_out[io_idx]
            original = f_m2[m2_idx]
            if original[2:] == i:
                i_list = i.split()
                o_list = o.split()
                m2_idx += 1
                shift = 0
                to_fix = []
                special = False
                while f_m2[m2_idx].startswith('A '):
                    temp = f_m2[m2_idx].split("|||")
                    temp[0] = temp[0].split()
                    if int(temp[0][2]) - int(temp[0][1]) > 1 or len(
                            temp[2].split()) > 1:
                        special = True
                        m2_idx += 1
                        continue
                    to_fix.append(
                        [int(temp[0][1]),
                         int(temp[0][2]), temp[1], temp[2]])
                    m2_idx += 1
                if special:
                    special_errors.append(original)
                    special_errors.append("\n")
                    while m2_idx < len(
                            f_m2) and not f_m2[m2_idx].startswith('S '):
                        m2_idx += 1
                    continue
                if count == check:
                    corrected = defaultdict(int)
                    errors = defaultdict(int)
                    print(i_list)
                    print()
                    print(o_list)
                    print()
                    print(to_fix)
                spell_error = False
                for s, e, t, res in to_fix:
                    if t == "noop":
                        if i == o:
                            corrected[t] += 1
                        else:
                            errors[t] += 1
                        continue
                    if count == check:
                        print(s, e, res, shift)
                    if not res:
                        if count == check:
                            print(i_list[s:e], o_list[s + shift:e + shift])
                        if i_list[s:e] == o_list[s + shift:e + shift]:
                            errors[t] += 1
                        else:
                            corrected[t] += 1
                            shift -= e - s
                    else:
                        if s == e:
                            if count == check:
                                print(
                                    o_list[s + shift:e + shift +
                                           len(res.split())], res.split())
                            if o_list[s + shift:e + shift +
                                      len(res.split())] != res.split():
                                errors[t] += 1
                            else:
                                corrected[t] += 1
                                shift += len(res.split())
                        else:
                            if count == check:
                                print(
                                    o_list[s + shift:s + shift +
                                           len(res.split())], res.split())
                            if o_list[s + shift:s + shift +
                                      len(res.split())] == res.split():
                                corrected[t] += 1
                                if s - e != len(res.split()):
                                    shift += len(res.split()) - (e - s)
                            else:
                                if len(t.split(":")) > 1 and t.split(
                                        ":")[1] == "ORTH":
                                    print(i, o)
                                errors[t] += 1
                                if i_list[s:e] != o_list[s + shift:e + shift]:
                                    shift += len(res.split()) - (e - s)
                                if t.split(":")[1] == "SPELL":
                                    spell_error = True
            while m2_idx < len(f_m2) and not f_m2[m2_idx].startswith('S '):
                m2_idx += 1
            io_idx += 1
            count += 1
            if count == check + 1:
                print(errors)
                print(corrected)
    # print(count)
    # print(special_errors)
    return errors, corrected


# Example usage:
input_file = "ABCN.dev.gold.bea19_original_typo.txt"
processed_in = 'typo_original.txt'
output = "typo_original_out.txt"
errors, correct = get_errors_and_correction(input_file, processed_in, output)
error_combined, correct_combined = defaultdict(int), defaultdict(int)
total = defaultdict(int)
error_ratio = defaultdict(int)
for key in errors:
    temp = key.split(':')
    if len(temp) == 1:
        total[key] += errors[key]
        error_combined[key] += errors[key]
    else:
        total[temp[1]] += errors[key]
        error_combined[temp[1]] += errors[key]

for key in correct:
    temp = key.split(':')
    if len(temp) == 1:
        total[key] += correct[key]
        correct_combined[key] += correct[key]

    else:
        total[temp[1]] += correct[key]
        correct_combined[temp[1]] += correct[key]

## the below 4 lines of code is specifically applicable for base gector model analysis only. Please remove it and edit code as necessary
total["CONJ"] = 38
error_combined["CONJ"] = 36
correct_combined["CONJ"] = 2
error_combined["SPELL"] += 2

for key in total:
    error_ratio[key] = int(100 * error_combined[key] / total[key])

print(total["OTHER"], total["ADV"], total["PART"])
print(error_combined)
print(correct_combined)


def plot_and_save(data, filename, title, y_label):
    keys = list(data.keys())
    values = list(data.values())
    plt.bar(keys, values)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.savefig(filename)
    plt.close()


plot_and_save(error_combined, 'errors.png',
              'Gector base model failed correction', "count")
plot_and_save(correct_combined, 'corrections.png',
              'Gector base model successful correction', "count")
plot_and_save(error_ratio, 'error_rate.png', 'Gector base model error rate',
              "percentage(%)")
