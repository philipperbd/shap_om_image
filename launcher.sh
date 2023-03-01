mkdir $1/Visuals
mkdir $1/Stats_outputs
python shap_dict.py --input $1/$2 --output $1/shap.json
echo "shap.json created at $1"
python minmaxscaler.py --input $1/shap.json
echo "shap_scalled.json created at $1"
python stats.py --path $1/
echo "stats.json created at $1"
python visuals.py --path $1
echo "visuals created at $1/Visuals/"