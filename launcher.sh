echo "--Start--"
source venv/bin/activate
echo "Virtual environment activated."
rm -rf $1/Visuals
rm -rf $1/Stats_outputs
echo "Cleaning done!"
mkdir $1/Visuals
mkdir $1/Stats_outputs
echo "New directories created at $1"
python shap_dict.py --input $1/$2 --output $1/shap.json
echo "shap.json done."
python minmaxscaler.py --input $1/shap.json
echo "shap_scalled.json done."
python stats.py --path $1/
echo "stats.json done."
python visuals.py --path $1 --image $3
echo "visuals done."
deactivate
echo "Virtual environment deactivated."
echo "--End--"