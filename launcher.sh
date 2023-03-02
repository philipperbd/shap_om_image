echo "--Start--"
source venv/bin/activate
echo "Virtual environment activated."
rm -rf data/$1/baby_visuals
rm -rf data/$1/stats_plots
rm data/$1/shap.json data/$1/shap_scalled.json data/$1/stats.json
echo "Cleaning done!"
mkdir data/$1/baby_visuals
mkdir data/$1/stats_plots
echo "New directories created at $1"
python scripts/shap_dict.py --input data/$1/$2 --output data/$1/shap.json
echo "shap.json done."
python scripts/minmaxscaler.py --input data/$1/shap.json
echo "shap_scalled.json done."
python scripts/stats_dict.py --path data/$1/
echo "stats.json done."
python scripts/stats_plots.py --path data/$1/
echo "stats visuals done."
python scripts/visuals.py --path data/$1 --image data/baby.png
echo "baby visuals done."
zip -r reports/$1_$2.zip data/$1/stats_plots data/$1/baby_visuals &> /dev/null
echo "report zip folder done."
deactivate
echo "Virtual environment deactivated."
echo "--End--"