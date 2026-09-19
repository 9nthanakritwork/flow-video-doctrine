#!/usr/bin/env python3
"""Pre-Flight Guard & Assertion Validator for Flow Video Production
Ensures strict adherence to the Boss Standard Flow Video Doctrine before issuing API calls.
Prevents accidental credit loss and wrong video mode selection.
"""

import sys

# Whitelist of approved 0-credit or intentional models
BANNED_MODELS = {
    "veo_3_1_i2v_s_fast_ultra": "โมเดลนี้กินเครดิต Ultra สูงมาก ห้ามใช้ในลูปผลิตอัตโนมัติเด็ดขาด!",
    "veo_3_1_t2v": "โมเดลนี้กิน 100 เครดิต ห้ามใช้เด็ดขาด!"
}

ALLOWED_GRID_MODES = {"r2v"}

class DoctrineViolationError(Exception):
    """Raised when a production script violates the Flow Video Doctrine."""
    pass

def validate_video_request(mode, model_key, reference_media_ids=None, has_grid=False, prompt=""):
    """Validates video generation payload against Doctrine rules before API dispatch.
    
    Args:
        mode (str): 't2v', 'i2v', 'r2v'
        model_key (str): Flow model key string
        reference_media_ids (list): List of media IDs attached to the video
        has_grid (bool): True if a storyboard grid was generated for this clip
        prompt (str): Video prompt text
    """
    reference_media_ids = reference_media_ids or []
    
    # 1. Credit Protection Guard
    if model_key in BANNED_MODELS:
        raise DoctrineViolationError(f"❌ [Credit Protection Blocked]: {BANNED_MODELS[model_key]}")
    
    # 2. Storyboard Grid Mode Guard
    if has_grid:
        if mode not in ALLOWED_GRID_MODES:
            raise DoctrineViolationError(
                f"❌ [Wrong Video Mode]: เมื่อมีภาพ Storyboard Grid ต้องใช้โหมด 'r2v' (Ingredients to Video / องค์ประกอบ) เท่านั้น! "
                f"แต่ในโค้ดระบุ mode='{mode}'"
            )
        if len(reference_media_ids) < 1:
            raise DoctrineViolationError(
                "❌ [Missing Grid Reference]: มีภาพ Storyboard Grid แต่ไม่ได้ส่ง mediaId ของภาพ Grid เข้าไปใน referenceMediaIds!"
            )
        if len(reference_media_ids) < 2:
            print("⚠️ [Warning]: ควรส่งทั้ง [รูปสินค้า Shopee] และ [รูปภาพ Storyboard Grid] รวม 2 รูปเข้าไปใน referenceMediaIds เพื่อความแม่นยำสูงสุด")

    # 3. Phone in Frame Check
    forbidden_terms = ["holding phone", "smartphone in hand", "holding smartphone", "holding camera"]
    for term in forbidden_terms:
        if term in prompt.lower():
            raise DoctrineViolationError(f"❌ [Visual Rule Violation]: พบคำสั่งที่มีโทรศัพท์ในมือ ('{term}') ใน Prompt! กฎเหล็กคือ Empty Hands ห้ามมีจอมือถือในเฟรมเด็ดขาด!")

    print(f"✅ [Pre-Flight Guard]: Payload validation PASSED (Mode: {mode}, Model: {model_key}, Refs: {len(reference_media_ids)})")
    return True

def validate_voiceover_script(script):
    """Validates Thai TTS voiceover script against Doctrine rules.
    
    Args:
        script (str): Voiceover text in Thai
    """
    # 1. Ban 100%
    if "100%" in script or "ร้อยเปอร์เซ็นต์" in script or "100 %" in script:
        raise DoctrineViolationError("❌ [Voiceover Violation]: พบคำว่า '100%' ในบทพูด! กฎเหล็กเจ้านายห้ามพูดคำว่า 100% เด็ดขาด ให้ใช้คำว่า 'สบายหายห่วง' หรือ 'มั่นใจได้เลย' แทน")

    # 2. Max 1 'ครับ'
    krub_count = script.count("ครับ")
    if krub_count > 1:
        raise DoctrineViolationError(f"❌ [Voiceover Violation]: พบบทพูดมีคำว่า 'ครับ' {krub_count} ครั้ง! กฎเหล็กกำหนดให้มีได้สูงสุดเพียง 1 ครั้งที่ท้ายคลิปเท่านั้น")

    print(f"✅ [Pre-Flight Guard]: Voiceover script validation PASSED ({len(script)} chars, 'ครับ': {krub_count})")
    return True

if __name__ == "__main__":
    print("Testing Pre-Flight Guard...")
    try:
        validate_voiceover_script("ปูแผ่นกันลื่นตัวนี้ สบายหายห่วง ปลอดภัย 100% ครับ")
    except DoctrineViolationError as e:
        print("Expected violation caught:", e)

    try:
        validate_video_request(mode="t2v", model_key="veo_3_1_t2v_lite", has_grid=True)
    except DoctrineViolationError as e:
        print("Expected violation caught:", e)

    print("Preflight Guard ready for import!")
