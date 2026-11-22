"""
Treatment recommendations for all 38 PlantVillage disease classes.
Each entry has:
  - description : short plain-English explanation of the disease
  - severity    : "low" | "medium" | "high"
  - steps       : ordered list of actionable treatment / prevention steps
"""

TREATMENTS: dict[str, dict] = {
    # ─── Apple ───────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "description": "Fungal disease (Venturia inaequalis) causing olive-green to black scab lesions on leaves and fruit.",
        "severity": "medium",
        "steps": [
            "Remove and destroy infected leaves and fallen debris — do not compost them.",
            "Apply a copper-based or lime-sulfur fungicide at bud-break and repeat every 7–10 days during wet weather.",
            "Use an approved myclobutanil or captan fungicide spray as an alternative.",
            "Prune to improve air circulation and reduce leaf wetness.",
            "Plant scab-resistant apple varieties (e.g., Liberty, Enterprise) for long-term management.",
            "Avoid overhead irrigation; water at the base of the tree.",
        ],
    },
    "Apple___Black_rot": {
        "description": "Fungal disease (Botryosphaeria obtusa) causing circular brown rot on fruit and leaf spots.",
        "severity": "high",
        "steps": [
            "Prune out all dead or cankered wood at least 15 cm below visible infection; disinfect pruning tools between cuts.",
            "Remove mummified fruits from the tree and ground immediately.",
            "Apply captan or thiophanate-methyl fungicide from pink-bud stage through harvest.",
            "Maintain tree vigor with balanced fertilization — stressed trees are more susceptible.",
            "Control fire blight and other wounds that serve as infection entry points.",
            "Dispose of pruned material away from the orchard.",
        ],
    },
    "Apple___Cedar_apple_rust": {
        "description": "Fungal disease (Gymnosporangium juniperi-virginianae) causing bright orange-yellow spots on leaves.",
        "severity": "medium",
        "steps": [
            "Remove nearby Eastern red cedar or juniper trees if feasible — they are the alternate host.",
            "Apply myclobutanil, trifloxystrobin, or propiconazole fungicide starting at pink-bud stage.",
            "Repeat fungicide applications every 7–10 days through the petal-fall stage.",
            "Plant rust-resistant apple varieties such as Liberty or Redfree.",
            "Rake and dispose of fallen leaves to reduce spore load.",
        ],
    },
    "Apple___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Continue regular scouting (weekly leaf inspections) to catch problems early.",
            "Maintain balanced irrigation and fertilization.",
            "Apply preventive dormant oil spray in late winter to control overwintering pests.",
            "Prune annually for good air circulation.",
        ],
    },

    # ─── Blueberry ───────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Maintain soil pH between 4.5 and 5.5 for optimal nutrient uptake.",
            "Mulch with pine bark or wood chips to retain moisture and suppress weeds.",
            "Scout regularly for signs of mummy berry, anthracnose, or stem blight.",
            "Apply balanced acid-forming fertilizer in early spring.",
        ],
    },

    # ─── Cherry ──────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "description": "Fungal disease (Podosphaera clandestina) producing white powdery coating on leaves and shoots.",
        "severity": "medium",
        "steps": [
            "Apply a sulfur-based or potassium bicarbonate fungicide at first sign of infection.",
            "Use myclobutanil or trifloxystrobin for more severe infections.",
            "Prune to improve air flow through the canopy.",
            "Avoid excess nitrogen fertilization which promotes lush, susceptible growth.",
            "Remove and dispose of infected shoots and leaves.",
            "Avoid overhead watering.",
        ],
    },
    "Cherry_(including_sour)___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout weekly during the growing season for powdery mildew, brown rot, and shot hole.",
            "Apply a preventive copper spray before bloom in wet seasons.",
            "Maintain good canopy airflow through annual pruning.",
        ],
    },

    # ─── Corn ────────────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "description": "Fungal disease (Cercospora zeae-maydis) causing rectangular gray to tan lesions on lower leaves.",
        "severity": "medium",
        "steps": [
            "Plant resistant hybrids — this is the most cost-effective long-term solution.",
            "Rotate corn with non-host crops (soybean, wheat) for at least one season.",
            "Till residue to accelerate decomposition of infected plant material.",
            "Apply a strobilurin (azoxystrobin) or triazole (propiconazole) fungicide at VT/R1 stage if disease pressure is high.",
            "Avoid late planting dates which increase humidity and disease risk.",
        ],
    },
    "Corn_(maize)___Common_rust_": {
        "description": "Fungal disease (Puccinia sorghi) producing small cinnamon-brown pustules on both leaf surfaces.",
        "severity": "medium",
        "steps": [
            "Plant rust-resistant corn hybrids.",
            "Scout fields from V6 stage onwards for early pustules.",
            "Apply a foliar fungicide (strobilurin or triazole) if rust appears before or at tasseling on susceptible hybrids.",
            "Ensure good field drainage to minimize leaf wetness.",
            "Avoid planting susceptible hybrids in regions with known high rust pressure.",
        ],
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Fungal disease (Exserohilum turcicum) causing long cigar-shaped gray-green to tan lesions on leaves.",
        "severity": "high",
        "steps": [
            "Use resistant hybrids carrying Ht genes.",
            "Rotate with non-host crops for 1–2 seasons.",
            "Apply azoxystrobin, propiconazole, or pyraclostrobin fungicide at VT/R1 if >50% of plants show lesions on or above the ear leaf.",
            "Destroy or bury corn residue after harvest to reduce inoculum.",
            "Avoid overhead irrigation if possible.",
        ],
    },
    "Corn_(maize)___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Continue regular scouting from V6 through grain fill.",
            "Maintain balanced nitrogen — excess N increases susceptibility to foliar diseases.",
            "Rotate crops to reduce soilborne and residue-borne pathogen build-up.",
        ],
    },

    # ─── Grape ───────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "description": "Fungal disease (Guignardia bidwellii) causing tan leaf lesions with dark borders and hard black mummified berries.",
        "severity": "high",
        "steps": [
            "Remove and destroy all mummified berries and infected canes during dormant pruning.",
            "Apply a protective fungicide (myclobutanil, mancozeb, or captan) from bud-break through 4–5 weeks post-bloom.",
            "Spray on a 7–10 day schedule, shortening to 5–7 days during wet weather.",
            "Train vines for maximum air circulation and sunlight penetration.",
            "Avoid wounds during wet periods — infections enter through wounds.",
        ],
    },
    "Grape___Esca_(Black_Measles)": {
        "description": "Complex wood disease caused by multiple fungi causing tiger-stripe leaf symptoms and berry spotting.",
        "severity": "high",
        "steps": [
            "There is no curative treatment — focus on prevention and slowing spread.",
            "Prune during dry conditions; make clean cuts and immediately protect large wounds with wound sealant containing thiophanate-methyl.",
            "Remove and destroy severely infected vines to prevent spread.",
            "Avoid water stress — maintain consistent irrigation.",
            "Disinfect pruning tools with 70% alcohol or 10% bleach solution between vines.",
            "Consider replanting with certified disease-free vines in heavily affected blocks.",
        ],
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "description": "Fungal disease (Isariopsis clavispora) causing angular dark brown spots that turn leaf edges papery and dry.",
        "severity": "medium",
        "steps": [
            "Remove infected leaves and dispose of them away from the vineyard.",
            "Apply mancozeb or copper-based fungicides when symptoms first appear.",
            "Improve air circulation by shoot positioning and leaf removal in the fruit zone.",
            "Avoid overhead irrigation.",
            "Apply preventive sprays during wet, warm weather periods.",
        ],
    },
    "Grape___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout weekly for early signs of black rot, downy mildew, and powdery mildew.",
            "Apply dormant copper spray before bud-break in disease-prone regions.",
            "Maintain a consistent spray program during wet seasons.",
            "Thin shoots and leaves for good air circulation.",
        ],
    },

    # ─── Orange ──────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "description": "Deadly bacterial disease (Candidatus Liberibacter asiaticus) spread by the Asian citrus psyllid causing yellow shoots and misshapen bitter fruit.",
        "severity": "high",
        "steps": [
            "There is currently NO cure — infected trees will decline and die.",
            "Remove and destroy infected trees immediately to prevent psyllid spread to healthy trees.",
            "Control the Asian citrus psyllid vector with imidacloprid soil drenches or foliar sprays of malathion/spinosad.",
            "Plant certified disease-free nursery stock only.",
            "Inspect new trees carefully before planting.",
            "Report suspected cases to your local agricultural extension office immediately.",
            "Consider thermotherapy treatments for mildly affected budwood material.",
        ],
    },

    # ─── Peach ───────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "description": "Bacterial disease (Xanthomonas arboricola pv. pruni) causing water-soaked lesions on leaves, fruit, and twigs.",
        "severity": "medium",
        "steps": [
            "Apply copper hydroxide or copper sulfate sprays starting at bud-swell and repeat every 10–14 days during wet weather.",
            "Avoid high-nitrogen fertilization which promotes susceptible lush growth.",
            "Plant resistant or tolerant varieties (e.g., Contender, Redhaven).",
            "Prune out infected twigs during dry conditions and disinfect tools.",
            "Maintain good air circulation through proper pruning.",
            "Avoid overhead irrigation.",
        ],
    },
    "Peach___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Apply dormant copper spray and oil in late winter.",
            "Scout regularly for bacterial spot, brown rot, and peach leaf curl.",
            "Thin fruit early to reduce crowding and improve air flow.",
            "Prune annually to maintain an open vase shape.",
        ],
    },

    # ─── Pepper ──────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "description": "Bacterial disease (Xanthomonas campestris pv. vesicatoria) causing water-soaked leaf spots that turn dark brown with yellow halos.",
        "severity": "medium",
        "steps": [
            "Apply copper-based bactericide (copper hydroxide + mancozeb) on a 5–7 day schedule during wet weather.",
            "Use certified disease-free or treated seed.",
            "Rotate peppers with non-host crops (corn, beans) for 2–3 years.",
            "Avoid working in the field when foliage is wet to reduce spreading.",
            "Remove and destroy infected plant debris after harvest.",
            "Plant resistant varieties where available.",
        ],
    },
    "Pepper,_bell___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout weekly for bacterial spot and anthracnose during wet seasons.",
            "Maintain consistent soil moisture — avoid drought stress.",
            "Apply balanced fertilizer; avoid excess nitrogen.",
            "Rotate crops each season.",
        ],
    },

    # ─── Potato ──────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "description": "Fungal disease (Alternaria solani) causing dark brown target-ring lesions on older lower leaves.",
        "severity": "medium",
        "steps": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin fungicide on a 7–10 day schedule when conditions favor infection.",
            "Remove and destroy infected lower leaves early in the season.",
            "Rotate potatoes with non-solanaceous crops for 2–3 years.",
            "Maintain adequate potassium and avoid plant stress — stressed plants are more susceptible.",
            "Plant certified seed tubers and resistant varieties.",
            "Avoid overhead irrigation in the evening.",
        ],
    },
    "Potato___Late_blight": {
        "description": "Oomycete disease (Phytophthora infestans) causing rapidly spreading dark water-soaked lesions — the cause of the Irish Famine.",
        "severity": "high",
        "steps": [
            "Act IMMEDIATELY — late blight can destroy a field in days under cool, wet conditions.",
            "Apply mancozeb, chlorothalonil, or cymoxanil + mancozeb fungicide on a 5–7 day schedule.",
            "Switch to a systemic fungicide (metalaxyl, dimethomorph) if the disease is already established.",
            "Destroy infected plant material — do not compost; burn or bury deep.",
            "Hill soil around plants to protect tubers from zoospores.",
            "Harvest tubers only when the foliage is fully dry to prevent tuber infection.",
            "Rotate with non-solanaceous crops for at least 3 years.",
            "Plant certified blight-resistant varieties.",
        ],
    },
    "Potato___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout fields twice weekly during cool, wet weather for late blight.",
            "Use certified disease-free seed potatoes.",
            "Apply preventive fungicide sprays during high-risk weather periods.",
            "Maintain good drainage to prevent waterlogged conditions.",
        ],
    },

    # ─── Raspberry ───────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Remove and destroy old floricanes after fruiting to reduce disease inoculum.",
            "Scout for gray mold, anthracnose, and spur blight.",
            "Ensure rows are not overcrowded — thin canes for air circulation.",
            "Apply preventive copper spray in early spring.",
        ],
    },

    # ─── Soybean ─────────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout weekly from V3 through R6 for sudden death syndrome, frogeye leaf spot, and soybean rust.",
            "Rotate soybean with corn to manage soilborne pathogens.",
            "Use certified seed treated with fungicide/insecticide.",
            "Maintain proper plant population and row spacing for air circulation.",
        ],
    },

    # ─── Squash ──────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "description": "Fungal disease causing white powdery coating on upper leaf surfaces, reducing photosynthesis.",
        "severity": "medium",
        "steps": [
            "Apply potassium bicarbonate, neem oil, or sulfur-based fungicide at first sign of infection.",
            "Use myclobutanil or trifloxystrobin for more severe infections.",
            "Avoid excess nitrogen fertilization.",
            "Plant resistant varieties (e.g., Butternut hybrids).",
            "Space plants adequately for air flow.",
            "Water at the base of plants — avoid wetting foliage.",
        ],
    },

    # ─── Strawberry ──────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "description": "Fungal disease (Diplocarpon earlianum) causing small dark purple spots that enlarge with brown centers giving a scorched appearance.",
        "severity": "medium",
        "steps": [
            "Remove and destroy infected leaves — rake and dispose of fallen material.",
            "Apply captan or myclobutanil fungicide on a 10–14 day schedule.",
            "Renovate plantings after harvest by mowing and thinning to improve air circulation.",
            "Avoid overhead irrigation; use drip irrigation.",
            "Plant resistant varieties where available.",
            "Do not set plants in areas with a history of leaf scorch without rotation.",
        ],
    },
    "Strawberry___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout regularly for gray mold (Botrytis), leaf scorch, and angular leaf spot.",
            "Remove old leaves and debris after harvest.",
            "Apply preventive fungicide before bloom if wet weather is forecast.",
            "Renovate planting each year after fruiting.",
        ],
    },

    # ─── Tomato ──────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "description": "Bacterial disease (Xanthomonas spp.) causing small water-soaked leaf spots that turn dark brown with yellow halos.",
        "severity": "medium",
        "steps": [
            "Apply copper hydroxide + mancozeb spray on a 5–7 day schedule during wet weather.",
            "Use certified disease-free seed or treat seed with hot water (50 °C for 25 minutes).",
            "Rotate tomatoes with non-solanaceous crops for 2 years.",
            "Avoid working in the field when plants are wet.",
            "Remove infected plant tissue; destroy crop debris after harvest.",
            "Avoid overhead irrigation.",
        ],
    },
    "Tomato___Early_blight": {
        "description": "Fungal disease (Alternaria solani) causing target-spot lesions with concentric rings on lower leaves.",
        "severity": "medium",
        "steps": [
            "Remove infected lower leaves as soon as symptoms appear.",
            "Apply chlorothalonil, mancozeb, or azoxystrobin on a 7–10 day schedule.",
            "Stake or cage plants to keep foliage off the ground.",
            "Mulch around the base to prevent soil splash onto lower leaves.",
            "Rotate with non-solanaceous crops for 2–3 years.",
            "Avoid overhead irrigation in the evening.",
        ],
    },
    "Tomato___Late_blight": {
        "description": "Oomycete disease (Phytophthora infestans) causing large dark water-soaked lesions on leaves and stems — spreads extremely rapidly.",
        "severity": "high",
        "steps": [
            "Act IMMEDIATELY — late blight can destroy a crop within a week.",
            "Apply mancozeb, chlorothalonil, or cymoxanil + mancozeb fungicide on a 5–7 day schedule.",
            "Switch to a systemic fungicide (metalaxyl or dimethomorph) for established infections.",
            "Remove and destroy ALL infected plant material — burn or bag and dispose; do NOT compost.",
            "Stake plants to improve air flow and reduce leaf wetness.",
            "Avoid any overhead watering — switch to drip irrigation.",
            "Plant resistant varieties (e.g., Mountain Merit, Defiant) next season.",
        ],
    },
    "Tomato___Leaf_Mold": {
        "description": "Fungal disease (Passalora fulva) causing olive-green to gray mold on the underside of leaves, yellow on top.",
        "severity": "medium",
        "steps": [
            "Reduce greenhouse humidity below 85% — improve ventilation.",
            "Apply chlorothalonil, mancozeb, or copper-based fungicide.",
            "Remove and destroy infected leaves.",
            "Avoid overhead watering; water in the morning.",
            "Space plants for maximum air circulation.",
            "Plant resistant varieties (e.g., with Cf genes) for greenhouse production.",
        ],
    },
    "Tomato___Septoria_leaf_spot": {
        "description": "Fungal disease (Septoria lycopersici) causing small circular spots with dark borders and light centers on lower leaves.",
        "severity": "medium",
        "steps": [
            "Remove infected lower leaves immediately — do not compost.",
            "Apply chlorothalonil, mancozeb, or copper-based fungicide on a 7–10 day schedule.",
            "Stake plants to keep foliage off the soil.",
            "Mulch the soil surface to prevent spore splash.",
            "Rotate with non-solanaceous crops for 2–3 years.",
            "Avoid overhead irrigation.",
        ],
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "description": "Arachnid pest (Tetranychus urticae) causing stippled bronze-yellow leaves with fine webbing on the underside.",
        "severity": "medium",
        "steps": [
            "Spray plants forcefully with water to dislodge mites — repeat every 2–3 days.",
            "Apply insecticidal soap, neem oil, or horticultural oil — ensure underside coverage.",
            "Use miticide (abamectin, bifenazate) for severe infestations.",
            "Introduce predatory mites (Phytoseiulus persimilis) as biological control.",
            "Avoid excess nitrogen fertilization — it promotes populations.",
            "Remove heavily infested leaves and dispose of them.",
            "Keep plants well-watered — drought stress worsens mite outbreaks.",
        ],
    },
    "Tomato___Target_Spot": {
        "description": "Fungal disease (Corynespora cassiicola) causing brown target-like concentric ring lesions on leaves and fruit.",
        "severity": "medium",
        "steps": [
            "Apply azoxystrobin, chlorothalonil, or mancozeb fungicide on a 7–10 day schedule.",
            "Remove and destroy infected plant material.",
            "Stake and train plants for good air circulation.",
            "Avoid overhead watering.",
            "Rotate with non-solanaceous crops.",
            "Scout fields regularly from early season to catch infection before it spreads.",
        ],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "Viral disease (TYLCV) transmitted by whiteflies, causing leaf curling, yellowing, and severe yield loss.",
        "severity": "high",
        "steps": [
            "There is NO cure for infected plants — remove and destroy them immediately.",
            "Control the silverleaf whitefly vector using imidacloprid, thiamethoxam, or spinosad insecticides.",
            "Use reflective silver mulches to repel whiteflies.",
            "Install 50-mesh insect-proof screens in greenhouses.",
            "Plant TYLCV-resistant varieties (e.g., Hazera, Seminis resistant lines).",
            "Inspect transplants carefully — do not introduce infected transplants.",
            "Eliminate solanaceous weed hosts near the field.",
        ],
    },
    "Tomato___Tomato_mosaic_virus": {
        "description": "Viral disease (ToMV) causing mosaic mottling, leaf distortion, and stunting — spread by contact.",
        "severity": "high",
        "steps": [
            "Remove and destroy infected plants immediately.",
            "Wash hands thoroughly with soap before and after handling plants.",
            "Disinfect all tools, stakes, and equipment with 10% bleach or 70% alcohol solution.",
            "Do NOT use tobacco products near tomatoes — ToMV can be carried in tobacco.",
            "Plant resistant varieties (e.g., with Tm-2 gene).",
            "Control aphid and other insect vectors.",
            "Avoid unnecessary handling of plants, especially in wet conditions.",
        ],
    },
    "Tomato___healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "severity": "low",
        "steps": [
            "Scout plants twice weekly for early blight, late blight, and bacterial spot.",
            "Apply preventive copper or chlorothalonil spray before wet weather periods.",
            "Stake, mulch, and avoid overhead watering.",
            "Rotate tomatoes with non-solanaceous crops each season.",
        ],
    },
}


def get_treatment(class_name: str) -> dict:
    """Return treatment info for a given PlantVillage class label."""
    info = TREATMENTS.get(class_name)
    if info:
        return info
    # Fallback for unknown / future classes
    is_healthy = "healthy" in class_name.lower()
    return {
        "description": "No specific treatment data available for this class.",
        "severity": "low" if is_healthy else "medium",
        "steps": [
            "Consult your local agricultural extension officer for diagnosis.",
            "Take a physical sample to a plant disease diagnostic lab.",
            "Isolate affected plants to prevent potential spread.",
        ],
    }
