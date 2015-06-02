#! /bin/bash

cd `dirname $0`
source ~/.login

log_f="tt.log"

corres_py="insertCorrespondencesToDB.py"
tt_py="insertTTsToDB.py"

corres_data="TT_Correspondences_by_Supprt.txt"
tt_data="Cut_TT_by_Support.txt"

corres_link="https://dw-results.amazon.com/dw-platform/servlet/results?job_id=5348531&encoding=UTF8&mimeType=text"
tt_link="https://dw-results.amazon.com/dw-platform/servlet/results?job_id=5348467&encoding=UTF8&mimeType=text"

# Get tt and correspondences
if [[ ! -f "$corres_data" ]]; then
	wget --no-check-certificate --user $USERNAME --password $PASSWORD "$corres_link" -O $corres_data
fi
if [[ ! -f "$tt_data" ]]; then
	wget --no-check-certificate --user $USERNAME --password $PASSWORD "$tt_link" -O $tt_data
fi

echo [`date +'%Y-%m-%d %H:%M:%S'`] [Correspondences:] >>$log_f
if [[ -f "$corres_data" ]]; then
	python "$corres_py" >>$log_f
	corres_mv="TT_Correspondence_by_Supprt_"`date +'%Y%m%d%H%M%S'`".txt"
	mv "$corres_data" "$corres_mv" && \
	tar -rf "./old/TT_Correspondence_by_Supprt.tar" "$corres_mv" && \
	rm "$corres_mv"
else
	echo " No update." >>$log_f
fi

echo [`date +'%Y-%m-%d %H:%M:%S'`] [TTs:] >>$log_f
if [[ -f "$tt_data" ]]; then
	python "$tt_py" >>$log_f
	tt_mv="Cut_TT_by_Support_"`date +'%Y%m%d%H%M%S'`".txt"
	mv "$tt_data" "$tt_mv" && \
	tar -rf "./old/Cut_TT_by_Support.tar" "$tt_mv"  && \
	rm "$tt_mv"
else
	echo " No update." >>$log_f
fi

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
echo Done!