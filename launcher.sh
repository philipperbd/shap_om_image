
mkdir $1
echo $1
python shap_dict.py --input Data/V2/XGB_V2_face --output Data/V2/shap.json
python minmaxscaler.py --input Data/V2/shap.json
python stats.py --path Data/V2/
python visuals.py --path Data/V2