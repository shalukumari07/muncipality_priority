import json
import random

records = []

locations = [
    "ward 5",
    "ward 12",
    "hospital",
    "school",
    "market",
    "park",
    "railway station",
    "bus stand",
    "residential area"
]

templates = {

    "Roads & Potholes": {

        "High": [
            "Large pothole causing accidents near {}",
            "Road severely damaged near {}",
            "Deep pothole creating traffic hazard near {}",
            "Road collapse reported near {}",
            "Dangerous potholes causing vehicle damage near {}"
        ],

        "Medium": [
            "Multiple potholes observed near {}",
            "Road surface damaged near {}",
            "Uneven road causing inconvenience near {}",
            "Small potholes increasing near {}",
            "Cracked road reported near {}"
        ],

        "Low": [
            "Road markings faded near {}",
            "Request for road maintenance near {}",
            "Minor road cracks observed near {}",
            "Request to repaint road markings near {}",
            "Routine road inspection requested near {}"
        ]
    },

    "Water Supply": {

        "High": [
            "Major water pipeline burst affecting residents near {}",
            "Complete water supply disruption near {}",
            "Water main leakage flooding area near {}",
            "Large pipe rupture reported near {}",
            "Emergency water line failure near {}"
        ],

        "Medium": [
            "Low water pressure reported in {}",
            "Intermittent water supply near {}",
            "Water leakage observed near {}",
            "Residents reporting reduced water flow near {}",
            "Water supply issue affecting homes near {}"
        ],

        "Low": [
            "Minor leak from public tap near {}",
            "Request for additional water connection near {}",
            "Routine water maintenance requested near {}",
            "Public tap requires repair near {}",
            "Water meter inspection requested near {}"
        ]
    },

    "Drainage & Sewer": {

        "High": [
            "Open manhole posing safety risk near {}",
            "Sewer overflow reported near {}",
            "Broken manhole cover near {}",
            "Drain collapse creating hazard near {}",
            "Overflowing sewage near {}"
        ],

        "Medium": [
            "Drain blockage causing foul smell near {}",
            "Water stagnation due to clogged drain near {}",
            "Drain overflow during rainfall near {}",
            "Partially blocked sewer near {}",
            "Drainage issue reported near {}"
        ],

        "Low": [
            "Routine drain maintenance requested near {}",
            "Drain cleaning requested near {}",
            "Minor drainage issue near {}",
            "Preventive sewer maintenance required near {}",
            "Drain inspection requested near {}"
        ]
    },

    "Street Lighting": {

        "High": [
            "Several street lights not working near {}",
            "Complete street lighting failure near {}",
            "Dark road due to nonfunctional lights near {}",
            "Street lights off creating safety concerns near {}",
            "Electrical fault affecting street lights near {}"
        ],

        "Medium": [
            "Street light flickering near {}",
            "Dim street lighting reported near {}",
            "Street light malfunction observed near {}",
            "Intermittent lighting issue near {}",
            "Street lamp requires repair near {}"
        ],

        "Low": [
            "Request for additional street light near {}",
            "Street lighting improvement requested near {}",
            "Request to install lamp post near {}",
            "Need better lighting coverage near {}",
            "Street light upgrade requested near {}"
        ]
    },

    "Waste Management": {

        "High": [
            "Garbage has not been collected for 10 days near {}",
            "Large garbage accumulation near {}",
            "Waste overflow creating health risk near {}",
            "Uncollected garbage causing sanitation issues near {}",
            "Severe waste disposal problem near {}"
        ],

        "Medium": [
            "Community dustbin overflowing near {}",
            "Waste bin full and unattended near {}",
            "Garbage collection delayed near {}",
            "Overflowing public waste container near {}",
            "Waste management issue reported near {}"
        ],

        "Low": [
            "Request for additional dustbin near {}",
            "Need more waste bins near {}",
            "Dustbin maintenance requested near {}",
            "Request for garbage bin installation near {}",
            "Additional waste collection point requested near {}"
        ]
    }
}

id_counter = 1

for category, priorities in templates.items():

    for priority, complaints in priorities.items():

        for _ in range(133):

            text = random.choice(
                complaints
            ).format(
                random.choice(locations)
            )

            records.append({
                "id": id_counter,
                "complaint_text": text,
                "priority": priority,
                "category": category
            })

            id_counter += 1

while len(records) < 2000:

    category = random.choice(
        list(templates.keys())
    )

    priority = random.choice(
        list(
            templates[category].keys()
        )
    )

    text = random.choice(
        templates[category][priority]
    ).format(
        random.choice(locations)
    )

    records.append({
        "id": id_counter,
        "complaint_text": text,
        "priority": priority,
        "category": category
    })

    id_counter += 1

random.shuffle(records)

with open(
    "complaints.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        records,
        f,
        indent=2
    )

print(
    f"Generated {len(records)} records successfully."
)