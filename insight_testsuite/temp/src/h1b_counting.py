from csv import reader
from re import match
from os import walk

def header_index(arg, header):
    """Scan CSV header and return index of arg"""
    for i, ele in enumerate(header):
        if match(arg, ele):
            return i
    raise NameError('column not found')

def populate_indices(header):
    """Return dict of column indices based on CSV header

    Arguments:
    header -- the header string from the CSV
    """
    indices = {}
    indices['status'] = header_index('.*STATUS.*', header)
    indices['soc'] = header_index('.*SOC_CODE.*', header)
    indices['job_name'] = header_index('.*SOC_NAME.*', header)
    indices['job_state'] = header_index('.*(WORKSITE_STATE|WORKLOC1_STATE).*', header)
    return indices     
    
def check_soc_hyphen(soc):
    """Return SOC with missing hypen added"""
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
    """Return cleaned and truncated SOC"""
    soc_strip = soc.replace(' ', '')
    soc_hyphen = check_soc_hyphen(soc_strip)
    return soc_hyphen[:7]

def ratio_formatted(job_count, total):
    """Return formatted ratio as a percentage"""
    num = round(100 * float(job_count) / total, 1)
    return str(num) + '%'

def format_output(top_lst, header, total):
    """Return formatted output string

    Arguments:
    top_lst -- top 10 jobs or states and their count as an array of tuples
    header -- header string for the output
    total -- total number of certified applications
    """
    answer = [header]
    for job in top_lst:
        row = []
        row.append(job[0])
        row.append(str(job[1]))
        row.append(ratio_formatted(job[1], total))
        answer.append(';'.join(row))
    return "\n".join(answer)

def sort_top_ten_states(dct):
    """Return the top 10 states sorted by count then name
    
    Arguments:
    dct -- Dict of states and their counts of certified applications
    """
    sorted_dct = sorted(dct.items(), key=lambda kv: kv[1])
    
    sorted_alpha = []
    while len(sorted_alpha) < 10 and len(sorted_dct) > 0:
        group = []
        group.append(sorted_dct.pop())
        while len(sorted_dct) > 0 and group[0][1] == sorted_dct[-1][1]:
            group.append(sorted_dct.pop())
        sorted_alpha += sorted(group)
    
    return sorted_alpha[:10]

def sort_top_ten_occupations(counts, names):
    """Return the top 10 occupations sorted by count then name
    
    Arguments:
    counts -- Dict of occupation SOC and their counts of certified applications
    names -- Dict of occupation SOC and their occupation title
    """
    sorted_dct = sorted(counts.items(), key=lambda kv: kv[1])
    
    sorted_alpha = []
    while len(sorted_alpha) < 10 and len(sorted_dct) > 0:
        group = []
        group.append(sorted_dct.pop())
        while len(sorted_dct) > 0 and group[0][1] == sorted_dct[-1][1]:
            group.append(sorted_dct.pop())
        named_group = [ (names[soc], c) for soc, c in group ]
        sorted_alpha += sorted(named_group)
    
    return sorted_alpha[:10]

def occupation_analysis(data):
    """Return a string of the top 10 occupations 

    Arguments:
    data -- Dict that contains a dict of SOC and certified application counts, a dict of SOC and job title, and an integer of total certified applications
    """
    top_ten = sort_top_ten_occupations(data['occupation_count'], data['occupation_dict'])   
    head = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    return format_output(top_ten, head, data['certified_count'])
        
def state_analysis(data):
    """Return a string of the top 10 occupations 

    Arguments:
    data -- Dict that contains a dict states and certified application counts and an integer of total certified applications
    """
    top_ten = sort_top_ten_states(data['state_count'])
    head = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    return format_output(top_ten, head, data['certified_count'])

def collect_data_points():
    """Return dict of cleaned and valid data points"""
    files = []
    for (dirpath, dirnames, filenames) in walk('./input/'):
        files.extend(filenames)
    if 'README.md' in files:
        files.remove('README.md')
    
    with open('./input/' + files[0]) as f:
        lines = list(reader(f, delimiter=';'))

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
        job_state = line[indices['job_state']].upper()
        if not match('\d{2}-\d{4}', soc) or not match('^[A-Z]{2}$', job_state):
            continue
    
        certified_count += 1
    
        if soc not in occupation_dict:
            occupation_dict[soc] = job_name
            occupation_count[soc] = 0
        elif len(occupation_dict[soc]) == 0:
            occupation_dict[soc] = job_name
        occupation_count[soc] += 1
    
        if job_state not in state_count:
            state_count[job_state] = 0
        state_count[job_state] += 1
    return {
        'occupation_dict' : occupation_dict,
        'occupation_count': occupation_count,
        'state_count' : state_count,
        'certified_count': certified_count
    }        

def analyze_and_output(data):
    """Run analysis modules and write them to the output files"""
    occupation_file = open('./output/top_10_occupations.txt', 'w')  
    occupation_file.write(occupation_analysis(data))

    states_file = open('./output/top_10_states.txt', 'w')
    states_file.write(state_analysis(data))

def main():
    data = collect_data_points()
    analyze_and_output(data)
    
main()
