for i in {3..3};do
n=$(wc -l tags/${i}.tags | cut -d' ' -f1 ) 
echo ${n}
#condor_run "./get_hashtag_vocab.py output/hashtag_${i}s/ tags/${i}.tags 10"
#condor_run "./get_avg_hashvec.py data/${i}_extid/ output/vectors_${i}s/ output/avgvec_${i}s/ "
#condor_run "./inner_kld.py output/avgvec_${i}s/ data/${i}_extid/ output/vectors_${i}s/ output/inner_kld/${i}.inner_kld"
#./avgvec_kld.py output/avgvec_${i}s/ tags/${i}.tags output/inner_kld/${i}.inner_kld ref output/tagkld/${i}.kld
./get_tag_txt.py data/${i}_extid/ 1000 2000 output/text_${i}s/ tags/${i}.tags output/tagtex/${i}s
./get_tag_txt.py data/${i}_extid/ 2000 ${n} output/text_${i}s/ tags/${i}.tags output/tagtex/${i}s
done
