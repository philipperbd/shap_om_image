NOCOLOR='\033[0m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
DONE="${GREEN}done${NOCOLOR}"
ERROR="${RED}error${NOCOLOR}"

echo "${HELLO}"

echo "${BLUE}START${NOCOLOR}"

if ! source venv/bin/activate; then
     echo "Virtual environment activation: ${ERROR}"
else
     echo "Virtual environment ${YELLOW}activated${NOCOLOR}"
fi 2>/dev/null

if ! rm -rf data/$1/baby_visuals data/$1/stats_plots data/$1/shap.json data/$1/shap_scalled.json data/$1/stats.json;  then
    echo "Cleaning: ${ERROR}"
else
    echo "Cleaning: ${DONE}"
fi 2>/dev/null

if ! mkdir data/$1/baby_visuals data/$1/stats_plots; then
    echo "Init new directories: ${ERROR}"
else
    echo "Init new directories: ${DONE}"
fi 2>/dev/null

if ! python scripts/shap_dict.py --input data/$1/$2 --output data/$1/shap.json; then
     echo "Create dictionnary with shap values: ${ERROR}"
else
     echo "Create dictionnary with shap values: ${DONE}"
fi 2>/dev/null

if ! python scripts/minmaxscaler.py --input data/$1/shap.json; then
     echo "Min-max scaler on shap values: ${ERROR}"
else
     echo "Min-max scaler on shap values: ${DONE}"
fi 2>/dev/null

if ! python scripts/stats_dict.py --path data/$1/; then
     echo "Create dictionnary with statistics: ${ERROR}"
else
     echo "Create dictionnary with statistics: ${DONE}"
fi 2>/dev/null

if ! python scripts/stats_plots.py --path data/$1/; then
     echo "Generate statistics plots: ${ERROR}"
else
     echo "Generate statistics plots: ${DONE}"
fi 2>/dev/null

python scripts/visuals.py --path data/$1 --image data/baby.png   

if ! python scripts/visuals.py --path data/$1 --image data/baby.png; then
     echo "Generate baby visuals: ${ERROR}"
else
     echo "Generate baby visuals: ${DONE}"
fi 2>/dev/null

if ! zip -r reports/$1_$2.zip data/$1/stats_plots data/$1/baby_visuals &> /dev/null; then
     echo "Add every visuals and plots to a report folder: ${ERROR}"
else
     echo "Add every visuals and plots to a report folder: ${DONE}"
fi 2>/dev/null

if ! deactivate; then
     echo "Virtual environment deactivation: ${ERROR}"
else
     echo "Virtual environment ${YELLOW}deactivated${NOCOLOR}"
fi 2>/dev/null

echo "${BLUE}END${NOCOLOR}"