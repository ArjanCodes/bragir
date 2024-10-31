from enum import StrEnum

TOKEN_LIMIT = 1500

MODEL_TOKEN_LIMITS = {
    "gpt_4o": 128000,
    "gpt_4o_2024_08_06": 128000,
    "gpt_4o_mini": 128000,
    "gpt_4o_mini_2024_07_18": 128000,
    "gpt_4o_realtime_preview": 128000,
    "gpt_4o_audio_preview": 128000,
    "o1_preview": 128000,
    "o1_preview_2024_09_12": 128000,
    "o1_mini": 128000,
    "o1_mini_2024_09_12": 128000,
    "gpt_4_turbo": 128000,
    "gpt_4": 8192,
    "gpt_3.5_turbo": 16385,
}


class AIModel(StrEnum):
    GPT_4O = "gpt_4o"
    GPT_4O_2024_08_06 = "gpt_4o_2024_08_06"
    GPT_4O_MINI = "gpt_4o_mini"
    GPT_4O_MINI_2024_07_18 = "gpt_4o_mini_2024_07_18"
    GPT_4O_REALTIME_PREVIEW = "gpt_4o_realtime_preview"
    GPT_4O_AUDIO_PREVIEW = " gpt_4o_audio_preview"
    O1_PREVIEW = "01_preview"
    O1_PREVIEW_2024_09_12 = "01_preview_2024_09_12"
    O1_MINI = "01_mini"
    O1_MINI_2024_09_12 = "01_mini_2024_09_12"
    GPT_4_TURBO = "gp_4_turbo"
    GPT_4 = "gpt_4"
    GPT_3_5_TURBO = "gpt_3_5_turbo"
