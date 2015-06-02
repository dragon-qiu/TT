#! /bin/bash

cd `dirname $0`
source ~/.login

log_f="tt_test.log"

# Search tt by tags
# ps_cse="qubrian;mliamzn;jacobliu;jiakeshu;jacktian;penyu;pingaws;xphou;shunwang;thcao;xinjianl;limary;leiyan;liangaws;panzheng;ylaws"
# cs_tcsa="shlin;flaws;jingziy;jinpinl;lvsu;wwwei;yiminz;yingzaws"
# searchURL="https://tt.amazon.com/search?requester_login="$ps_cse";"$cs_tcsa"&search=Search!&output=csv&tags="
searchURL="https://tt.amazon.com/search?search=Search!&output=csv&tags="
TAGFILE="tags.txt"

if [[ -f "getTags.py" ]]; then
	python getTags.py -o "$TAGFILE"
else
	echo "No file: getTags.py"
fi

if [[ -f "$TAGFILE" ]]; then
	# for tag in `cat tags.txt`; do
	cat $TAGFILE | while read tag ; do
		if [[ -n "$tag" ]]; then
			echo [`date +'%Y-%m-%d %H:%M:%S'`] [Insert Tag] [$tag] >>$log_f
			wget --no-check-certificate --user $USERNAME --password $PASSWORD "$searchURL$tag" -O "TT_withTag_$tag.txt"
			python insertTagsToDB.py --tag="$tag" >>$log_f
			tag_mv="TT_withTag_$tag""_`date +'%Y%m%d%H%M%S'`"".txt"
			mv "TT_withTag_$tag.txt" "$tag_mv" && \
			tar -rf "./old/TT_withTag.tar" "$tag_mv" && \
			rm "$tag_mv"
		fi
	done
else
	echo "No file: $TAGFILE"
fi
