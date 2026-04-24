import fonttools

# bash for loop over ['Literata','Noto_Sans','Source_Sans_3','Source_Serif_4']
for font in Literata Noto_Sans Source_Sans_3 Source_Serif_4; do
    # strip _ from name
    name=${font//_/}
    # glob for name-VariableFont_*.ttf in local_font_cache
    files=$(ls ./local_font_cache/$font/$name-VariableFont_*.ttf)
    # get first
    file=$(echo $files | awk '{print $1}')
    # run fonttools varLib.instancer on file with wght=350 and output to waxwing/fonts/$font/static/$name-Book.ttf
    fonttools varLib.instancer $file wght=350 -o ./waxwing/fonts/$font/static/$name-Book.ttf
done