import csv
import re
from os import walk

def header_index(arg, header):
    for i, ele in enumerate(header):
        if re.match(arg, ele):
            return i
    raise NameError('column not found')

def populate_indices(header):
    indices = {}
    indices['status'] = header_index('.*STATUS.*', header)
    indices['soc'] = header_index('.*SOC_CODE.*', header)
    indices['job_name'] = header_index('.*SOC_NAME.*', header)
    indices['job_state'] = header_index('.*(WORKSITE_STATE|WORKLOC1_STATE).*', header)
    return indices     
    
def check_soc_hyphen(soc):
    if len(soc) < 6:
        return soc
    soc_lst = list(soc)
    
    if soc_lst[2] != '-':
        if soc_lst[2] == '.':
            soc_lst[2] = '-'
        else:
            soc_lst.insert(2, '-')
    return ''.join(soc_lst)

def clean_soc(soc):
    soc_strip = soc.replace(' ', '')
    soc_hyphen = check_soc_hyphen(soc_strip)
    return soc_hyphen[:7]

def ratio_formatted(job_count, total):
    num = round(100 * float(job_count) / total, 1)
    return str(num) + '%'

def sort_top_ten(dct):
    sorted_dct = sorted(dct.items(), key=lambda kv: kv[1])
    
    sorted_alpha = []
    while len(sorted_alpha) < 10 and len(sorted_dct) > 0:
        group = []
        group.append(sorted_dct.pop())
        while len(sorted_dct) > 0 and group[0][1] == sorted_dct[-1][1]:
            group.append(sorted_dct.pop())
        sorted_alpha += sorted(group)
    
    return sorted_alpha[:10]

def format_output(top_lst, header, total):
    answer = [header]
    for job in top_lst:
        row = []
        row.append(job[0])
        row.append(str(job[1]))
        row.append(ratio_formatted(job[1], total))
        answer.append(';'.join(row))
    return "\n".join(answer)

def occupation_analysis(count, names, total):
    named_count = {}
    for k,v in count.items():
        name = names[k]
        named_count[name] = v
    top_ten = sort_top_ten(named_count)
    
    head = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    return format_output(top_ten, head, total)
        
def state_analysis(count, total):
    top_ten = sort_top_ten(count)
    head = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    return format_output(top_ten, head, total)

def main():

    files = []
    for (dirpath, dirnames, filenames) in walk('./input/'):
        files.extend(filenames)
    files.remove('README.md')
    
    with open('./input/' + files[0]) as f:
        lines = list(csv.reader(f, delimiter=';'))

    occupation_dict = {}
    occupation_count = {}
    state_count = {}
    certified_count = 0
    indices = populate_indices(lines[0])
    
    for line in lines[1:]:
        if line[indices['status']] != 'CERTIFIED':
            continue    
        
        soc = clean_soc(line[indices['soc']])  
        job_name = line[indices['job_name']]
        job_state = line[indices['job_state']]
        if not re.match('\d{2}-\d{4}', soc) or job_state == '':
            continue
    
        certified_count += 1
    
        if soc not in occupation_dict:
            occupation_dict[soc] = job_name
            occupation_count[soc] = 0
        elif len(job_name) > len(occupation_dict[soc]):
            occupation_dict[soc] = job_name
        occupation_count[soc] += 1
    
        state = line[indices['job_state']]
        if state not in state_count:
            state_count[state] = 0
        state_count[state] += 1

    occupation_file = open('./output/top_10_occupations.txt', 'w')  
    occupation_file.write(occupation_analysis(occupation_count, occupation_dict, certified_count))

    states_file = open('./output/top_10_states.txt', 'w')
    states_file.write(state_analysis(state_count, certified_count))

main()
