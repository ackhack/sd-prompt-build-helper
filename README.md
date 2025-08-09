# Prompt Build Helper

Simple extension for [SD.Next](https://github.com/vladmandic/sdnext/) to help building and randomizing prompts.

## Usage
Currently, the prompts need to be definied via a config.json file located in your Data Directory under `extensions\prompt-build-helper\config.json`.

A simple example below:
```json
{
    "active":true,
    "base_model":"Illustrious",
    "categories":[
    {
        "name":"General",
        "active":true,
        "randomized": {
            "randomized": false,
            "max_prompts": -1,
            "min_prompts": -1
        },
        "type":"positive",
        "prompts": [
            {
                "name": "Anime Style",
                "active":true,
                "prompt": "masterpiece,best quality,amazing quality, anime,anime screencap,"
            }
        ]
    },
    {
        "name":"Character",
        "active":true,
        "randomized": {
            "randomized": true,
            "max_prompts": 1,
            "min_prompts": 1
        },
        "type":"positive",
        "prompts": [
            {
                "name": "Ganyu",
                "active":true,
                "prompt": "ganyu, medium breasts, horns, blue hair,"
            },
            {
                "name": "Akane Kurokawa",
                "active":true,
                "prompt": "akane kurokawa, kurokawa akane, long hair, bangs, blue eyes, green eyes, black hair, blue hair, multicolored hair, gradient hair,",
                "loras": [
                    {
                        "base_model_type": "Illustrious",
                        "name":"<lora:akane-kurokawa-s1s2-illustriousxl-lora-nochekaiser:1.0>"
                    }
                ]
            },
            {
                "name": "Miyako Saitou",
                "active":true,
                "prompt": "miyako saitou, saitou miyako, long hair, brown hair, brown eyes,",
                "loras": [
                    {
                        "base_model_type": "Illustrious",
                        "name":"<lora:miyako-saitou-s1-illustriousxl-lora-nochekaiser:1.0>"
                    }
                ]
            },
            {
                "name": "Priscilla Barielle",
                "active":true,
                "prompt": "priscilla barielle, long hair, blonde hair, red eyes, brown eyes, braid, side ponytail, braided bangs,",
                "loras": [
                    {
                        "base_model_type": "Illustrious",
                        "name":"<lora:priscilla-barielle-s3-p2-illustriousxl-lora-nochekaiser:1.0>"
                    }
                ]
            }
        ]
    },
    {
        "name":"Character Traits",
        "active":true,
        "randomized": {
            "randomized": true,
            "max_prompts": -1,
            "min_prompts": 1
        },
        "type":"positive",
        "prompts": [
            {
                "name": "Happy Face",
                "active":true,
                "prompt": "looking at viewer, smiling, blushing,"
            },
            {
                "name": "Sad Face",
                "active":true,
                "prompt": "looking at viewer, sad,"
            },
            {
                "name": "High Ponytail",
                "active":true,
                "prompt": "high ponytail,"
            }
        ]
    },
    {
        "name":"Scenes",
        "active":true,
        "randomized": {
            "randomized": true,
            "max_prompts": 1,
            "min_prompts": 1
        },
        "type":"positive",
        "prompts": [
            {
                "name": "Sitting",
                "active":true,
                "prompt": "sitting, chair,"
            },
            {
                "name": "Squatting",
                "active":true,
                "prompt": "squatting,"
            },
            {
                "name": "Jogging",
                "active":true,
                "prompt": "jogging, running,"
            }
        ]
    },
    {
        "name":"Backgrounds",
        "active":true,
        "randomized": {
            "randomized": true,
            "max_prompts": 1,
            "min_prompts": 1
        },
        "type":"positive",
        "prompts": [
            {
                "name": "Kitchen",
                "active":true,
                "prompt": "kitchen, inside,"
            },
            {
                "name": "Park",
                "active":true,
                "prompt": "outside, trees, park,"
            }
        ]
    },
    {
        "name":"Negatives",
        "active":true,
        "randomized": {
            "randomized": false,
            "max_prompts": 1,
            "min_prompts": 1
        },
        "type":"negative",
        "prompts": [
            {
                "name": "Default Negatives",
                "active":true,
                "prompt": "bad quality,worst quality,worst detail,sketch,censor"
            }
        ]
    }]
}
```