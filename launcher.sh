echo "--Start--"
source venv/bin/activate
echo "Virtual environment activated."
rm -rf $1/Visuals
rm -rf $1/Stats_outputs
rm $1/shap.json $1/shap_scalled.json $1/stats.json
echo "Cleaning done!"
mkdir $1/Visuals
mkdir $1/Stats_outputs
echo "New directories created at $1"
python shap_dict.py --input $1/$2 --output $1/shap.json
echo "shap.json done."
python minmaxscaler.py --input $1/shap.json
echo "shap_scalled.json done."
python stats_dict.py --path $1/
echo "stats.json done."
python stats_plots.py --path $1/
echo "stats visuals done."
python visuals.py --path $1 --image $3
echo "baby visuals done."
deactivate
echo "Virtual environment deactivated."
echo "--End--"