#!/bin/bash

config_file=resource.cfg
if [ ! -z $1 ]; then
    config_file=$1
fi

hadoop_path=''
hadoop_lib=''
input_list=''
input_format='text'
files=''
output_dir=''
outputformat='text'
overwrite='no'
numreducetasks=1
nummaptasks=''
memlimit=''

section=''

function get_value {                                                            
    echo ${1##*=}                                                               
}                                                                               
                                                                                
function get_pair {                                                             
    key=${1%%=*}                                                                
    value=${1##*=}                                                              
} 

function set_para {
    if [[ $1 == 'hadoop_path' ]]; then
        hadoop_path=$2

    elif [[ $1 == 'hadoop_lib' ]]; then
        hadoop_lib=$2

    elif [[ $1 == 'input_format' ]]; then
        input_format=$2

    elif [[ $1 == 'outputformat' ]]; then
        outputformat=$2

    elif [[ $1 == 'overwrite' ]]; then
        overwrite=$2

    elif [[ $1 == 'nummaptasks' ]]; then
        nummaptasks=$2

    elif [[ $1 == 'numreducetasks' ]]; then
        numreducetasks=$2

    elif [[ $1 == 'memlimit' ]]; then
        memlimit=$2

    elif [[ $1 == 'output_dir' ]]; then
        output_dir=$2

    elif [[ $1 == 'main_file' ]]; then
        main_file=$2
    fi
} 

function set_command {
    if [[ -z $1 ]]; then
        echo ""
    else
        echo "$2 $1"
    fi
}

while read line; do
    # '#' pass
    if [[ "$line" =~ ^# ]]; then
        continue
    fi
    
    #[[ "$line" =~ ^# ]] && continue

    # '[]' section
    if [[ "$line" =~ ^\[ ]]; then
        section=`echo $line | cut -d[ -f2 | cut -d] -f1 `
        continue
    fi

    # content
    if [[ $section == 'dependence' ]]; then
        new_file=$(get_value $line)
        files="$files $new_file"
    
    elif [[ $section == 'input' ]]; then
        new_path=$(get_value $line)
        input_list="$input_list $new_path"

    elif [[ $section == 'dumbo' ]]; then
        get_pair $line
        set_para $key $value
    fi
done < $config_file


dumbo_command="dumbo start $main_file"
dumbo_command="$dumbo_command $(set_command "$hadoop_path" -hadoop)"
dumbo_command="$dumbo_command $(set_command "$hadoop_lib" -hadooplib)"

dumbo_command="$dumbo_command $(set_command "$input_format" -inputformat)"

for input in $input_list
do
    dumbo_command="$dumbo_command $(set_command "$input" -input)"
done

dumbo_command="$dumbo_command $(set_command "$output_dir" -output)"
dumbo_command="$dumbo_command $(set_command "$outputformat" -outputformat)"

for file in $files
do
    dumbo_command="$dumbo_command $(set_command "$file" -file)"
done

dumbo_command="$dumbo_command $(set_command "$overwrite" -overwrite)"
dumbo_command="$dumbo_command $(set_command "$nummaptasks" -nummaptasks)"
dumbo_command="$dumbo_command $(set_command "$numreducetasks" -numreducetasks)"
dumbo_command="$dumbo_command $(set_command "$memlimit" -memlimit)"

echo $dumbo_command
$dumbo_command
