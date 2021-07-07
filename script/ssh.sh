query=$1

json='{"items": ['
jsonEnd=']}'

sshconfig="$(grep -w -i Host ~/.ssh/config | sed 's/Host //g')"

hosts=()

while read -r host; do
    if [ "${host}" = '*' ] ; then
        continue
    fi
    if [[ "${host}" == *"${query}"* ]] || [ ${query} = 'all' ]; then
      hosts+=("{\"title\": \"${host}\", \"autocomplete\": \"${host}\", \"arg\": \"${host}\"}")
    fi
done <<< "${sshconfig}"

if [ ${query} != 'all' ]; then
	hosts+=("{\"title\": \"${query}\", \"autocomplete\": \"${query}\", \"arg\": \"${query}\"}")
fi

items=$( IFS=','; echo "${hosts[*]}")

echo ${json}${items}${jsonEnd}
