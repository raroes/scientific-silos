# download citations from the Open Citation Index

export DOWNLOAD_URL="https://ndownloader.figshare.com/articles/6741422/versions/7"
export DESTINATION_FILE="./data/citation_data.zip"
export DESTINATION_FOLDER="./data/"

echo rm -f $DESTINATION_FILE
rm -f $DESTINATION_FILE

echo wget -q $DOWNLOAD_URL -O $DESTINATION_FILE
wget -q $DOWNLOAD_URL -O $DESTINATION_FILE

echo unzip -o $DESTINATION_FILE -d $DESTINATION_FOLDER
unzip -o $DESTINATION_FILE -d $DESTINATION_FOLDER
