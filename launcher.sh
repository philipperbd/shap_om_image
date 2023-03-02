NOCOLOR='\033[0m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'

DONE="${GREEN}done${NOCOLOR}"

echo "${BLUE}START${NOCOLOR}"

source venv/bin/activate
echo "Virtual environment ${YELLOW}activated${NOCOLOR}"

rm -rf data/$1/baby_visuals
rm -rf data/$1/stats_plots
rm data/$1/shap.json data/$1/shap_scalled.json data/$1/stats.json
echo "Cleaning ${DONE}"

mkdir data/$1/baby_visuals
mkdir data/$1/stats_plots
echo "Init new directories: ${DONE}"

python scripts/shap_dict.py --input data/$1/$2 --output data/$1/shap.json
echo "Create dictionnary with shap values: ${DONE}"

python scripts/minmaxscaler.py --input data/$1/shap.json
echo "Min-max scaler on shap values: ${DONE}"

python scripts/stats_dict.py --path data/$1/
echo "Create dictionnary with statistics: ${DONE}"

python scripts/stats_plots.py --path data/$1/
echo "Generate statistics plots: ${DONE}"

python scripts/visuals.py --path data/$1 --image data/baby.png
echo "Generate baby visuals: ${DONE}"

zip -r reports/$1_$2.zip data/$1/stats_plots data/$1/baby_visuals &> /dev/null
echo "Add every visuals and plots to a report folder: ${DONE}"

deactivate
echo "Virtual environment ${YELLOW}deactivated${NOCOLOR}"

echo "${BLUE}END${NOCOLOR}"