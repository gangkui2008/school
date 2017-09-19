#!/bin/ksh

# Be aware that the given .csv file may contain BOM(e.g. \xef\xbb\xbf) or carriage return
# So need to remove them when do comparison

#set -x

function usage {
    echo "Usage: $0 <school.csv>"
    echo "在提供的csv文件中，找到都是（市先进|市示范|市重点|省先进|省示范|省重点）的小学和对口中学，将它们输出到另一个csv文件中"
    exit 1
}

if [[ $# -lt 1 ]]
then
    usage
fi

src=$1
result="$(pwd)/goodSchool.csv"
empty="$(pwd)/empty_record_school.txt"
rm -rf $result
rm -rf $empty

total=$(wc -l $src | awk '{print $1}')
cur=0

while read line
do
    let cur=cur+1
    echo "$(Date) Processing $cur/$total"
    count=$(echo "$line" | egrep -c '市先进|市示范|省重点|省示范|省先进|市重点')
    xiaoxuecount=$(echo "$line" | awk -F ',' '{print $3}' | egrep -c '小学') # only search xiaoxue
    if [[ $count -gt 0 ]] && [[ $xiaoxuecount -gt 0 ]]
    then
        echo $line
        schools=$(echo "$line" | awk -F ',' '{print $10}') #chuzhong
        for school in $schools
        do
            school=$(echo $school | tr -d ' \r\n\t\b' | awk '{gsub(/\xef\xbb\xbf/,"")}{print}') #remove carriage return and BOM
            [[ -z "$school" ]] && continue
            SAVEIFS=$IFS
            IFS=$(echo -en "\n\b") #Below for loop won't work without changing IFS
            match_lines=$(egrep "$school" $src)
            find_match=0
            for m in $match_lines
            do
                name=$(echo $m | awk -F ',' '{print $1}' | tr -d ' \r\n\t\b' | awk '{gsub(/\xef\xbb\xbf/,"")}{print}')
                gaiyao=$(echo $m | awk -F ',' '{print $3}' | tr -d ' \r\n\t\b' | awk '{gsub(/\xef\xbb\xbf/,"")}{print}')
                count=$(echo $gaiyao | egrep -c "$school")
                if [[ "$name" == "$school" ]] || [[ $count -gt 0 ]]
                then
                    find_match=1
                    count=$(echo $m | egrep -c '市先进|市示范|省重点|省示范|省先进|市重点')
                    if [[ $count -gt 0 ]]
                    then
                        echo $line >> $result
                        echo $m >> $result
                        echo "" >> $result
                        echo "match: $m"
                    fi
                fi
            done
            IFS=$SAVEIFS
            if [[ $find_match -eq 0 ]] #Did not find any record for that school
            then
                echo $school >> $empty
            fi
        done
    fi
done < $src

echo
echo "All done. Please check file $result and $empty"

exit 0




