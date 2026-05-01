#!/usr/bin/env python3
"""
Mat & Vic's Ad Concept Image Generator — fal-ai/nano-banana-2
50 ad images for the "5 Reasons 100% Cotton Socks Are Designed to Fail You" presell funnel.
All images: 4:5 vertical. Headline = "5 Reasons 100% Cotton Socks Are Designed to Fail You" only.
No product name, no price, no sub-copy inside any image.
Avatar: European professional male 25–50, practical, responds to evidence.
Villain: 100% cotton fiber. Each concept attacks one of the 5 reasons.

Setup:
    pip install fal-client
    export FAL_KEY=your_key_here   # get from fal.ai/dashboard

Usage:
    python3 generate_ad_images.py --ids all
    python3 generate_ad_images.py --ids c01,c02
    python3 generate_ad_images.py --list
"""

import argparse
import os
import sys
import time
import urllib.request
from pathlib import Path
from datetime import datetime

try:
    import fal_client
except ImportError:
    fal_client = None

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "generated_images" / "ad-concepts"
DELAY_BETWEEN = 3

HEADLINE = "5 Reasons 100% Cotton Socks Are Designed to Fail You"

PROMPTS = [
    {
        "id": "c01",
        "concept": "01 — Glasses Man Close-Crop UGC (Reason 1: Elastic Memory)",
        "swipe_ref": "ID 071 — SCR-20260313-brbu.jpeg (testimonial-discovery)",
        "reason": 1,
        "prompt": '{"style":"UGC close-crop — intimate portrait with selfie energy. Phone-camera quality, slightly imperfect framing. The man is the credibility. The headline is the argument.","lighting":"Natural ambient — warm wall behind, side window light. Not corrected. Slightly warm or neutral.","scene":"Extreme close crop: man, mid-50s, round or classic rectangular glasses worn on face. Head and upper chest only. Slightly off-angle — not centred. He is NOT looking at camera — eyes cast slightly down or to the side, the expression of someone who figured something out and is mildly annoyed it took this long. Background: plain wall, bookshelf edge, or window behind him. Tight and slightly imperfect. Bold white headline text overlaid directly on lower half of the image.","primary_object":{"description":"The man and the headline together — both are the scroll-stop","glasses_detail":"Round or classic rectangular frames — worn on face, not held. Slightly smudged or lived-in is fine.","expression_detail":"Thoughtful, slightly sceptical, mild irritation — not angry, not smiling. The look of someone who read something that reframed twenty years of habit.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type, large, lower half of image directly on photo — no card, no scrim box","weight":"heavy/black"}},"supporting_objects":[],"energy":"Decades of the same habit. The headline is the revelation.","constraints":{"glasses_must_be_worn_on_face_not_held":true,"NOT_looking_at_camera_or_smiling":true,"extreme_close_crop_face_and_chest_only":true,"headline_directly_on_photo_no_card_no_scrim_box":true,"headline_is_the_only_text_in_image":true,"NOT_studio_or_professional_photo_quality":true}}',
        "negative_prompt": "looking at camera, smiling, studio lighting, professional portrait, stock photo expression, glasses held not worn, gym, athletic, fashion, text in card box, white background, cartoon, illustration, 3d render, badge, masthead, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c02",
        "concept": "02 — Heel Close-Up Macro (Reason 3: Uniform Construction)",
        "swipe_ref": "ID 083 — SCR-20260313-btab.jpeg (bathroom-mirror-handwritten-message, detail-shot register)",
        "reason": 3,
        "prompt": '{"style":"Editorial macro photography — tight crop, sharp detail. Looks like an investigative piece photo, not a product shot.","lighting":"Soft natural indoor light — window to the side. Neutral hardwood or tile floor surface. No harsh shadows. The texture of the fabric is the subject.","scene":"Extreme close-up of a foot wearing a cotton sock — shot from heel-level or slightly above. The heel area fills most of the frame. No person visible above the ankle. The heel shows a worn patch or thinning zone — the fabric is clearly thinner at the heel than at the cuff visible at the top of frame.","primary_object":{"description":"Cotton sock on foot — the heel damage is the focal point","sock_detail":"Dark navy or grey cotton sock. Heel area showing visible wear: thinner fabric, slightly pilled surface, or early hole forming. The worn zone is centred or dominant in frame.","floor_detail":"Hardwood or stone tile visible at the edge of frame. Practical indoor environment.","position":"Heel zone centred, foot at rest. No visible person above the ankle."},"supporting_objects":[],"energy":"The damage is already happening. You just have not looked yet.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type overlaid across the bottom third of image, high contrast against the dark sock","weight":"heavy/black"},"constraints":{"heel_damage_must_be_the_clear_focal_point":true,"NOT_clean_undamaged_sock":true,"NOT_above_ankle_in_frame":true,"floor_surface_visible_at_frame_edge":true,"no_brand_markings_on_sock":true,"NOT_studio_shot_or_white_background":true}}',
        "negative_prompt": "clean sock, undamaged sock, person above ankle, face, gym, athletic sock, colorful sock, studio shot, white background, lifestyle pose, cartoon, illustration, 3d render, badge, CTA button, brand name",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c03",
        "concept": "03 — Native Advertorial Text Card (Reason 1: Elastic Memory)",
        "swipe_ref": "ID 062 — SCR-20260313-bqhj.jpeg (native-advertorial-062)",
        "reason": 1,
        "prompt": '{"style":"Native ad composite — large bold text card over a real documentary photo background. Resembles a health or consumer news sponsored post, not a brand advertisement.","lighting":"Background: soft natural ambient, slightly warm — home interior hallway or entrance. Nothing studio.","scene":"Full-bleed background photo: a man in his 40s, slightly out of focus, in a practical indoor setting — pulling up his sock at the ankle in a hallway before leaving. He is background texture only. Foreground: white rounded-corner text card overlaid on lower two-thirds of image, like a news article card sitting over the photo. The card contains bold headline text only. Small circular author headshot bottom-left of card.","primary_object":{"description":"The white text card overlay — this is what the eye reads first","card_headline":"5 Reasons 100% Cotton Socks Are Designed to Fail You","card_note":"Headline only inside the card — no sub-deck, no body copy, no CTA","author_circle_detail":"Small circular photo bottom-left of card — real-looking man, 50s, slightly informal. No name text. No studio quality in the headshot."},"supporting_objects":[],"energy":"A news article someone shared because it made them feel less stupid.","constraints":{"white_card_overlay_must_cover_lower_two_thirds":true,"background_man_must_be_blurred_and_secondary":true,"man_in_background_pulling_up_sock_at_ankle":true,"card_contains_headline_only_no_sub_deck_no_body_copy":true,"card_must_look_like_editorial_article_card_not_banner_ad":true,"NOT_bright_vivid_background_colours":true}}',
        "negative_prompt": "sharp focused person as main subject, studio lighting, stock photo background, fashion model, CTA button in card, bright background colors, brand logo, cartoon, illustration, 3d render, badge, learn more button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c04",
        "concept": "04 — Ingredient Comparison Table (Reason 5: Fiber Degradation)",
        "swipe_ref": "ID 053 — SCR-20260313-bomg.png (ingredient-comparison)",
        "reason": 5,
        "prompt": '{"style":"Clean data-driven editorial graphic — resembles a nutritional label comparison table. Dark background, high contrast. Editorial not advertising.","lighting":"Not applicable — dark background, flat layout.","scene":"Dark charcoal or near-black background. Bold white headline text at top. Below: two-column comparison table. Left column: blend sock with three ingredient rows and green checkmarks. Right column: cotton-only sock with three rows — two show 0% with red X marks. Small sock image above each column header.","primary_object":{"description":"Two-column ingredient table","left_column":"Neat rolled dark sock image above header. Three rows: 78% Combed Cotton checkmark | 20% Polyamide checkmark | 2% Elastane checkmark. Left column header has a subtle teal tint.","right_column":"Single plain light-coloured sock above header. Three rows: 100% Cotton neutral | 0% Polyamide X | 0% Elastane X. Red X marks on the zero-percent rows are the focal point.","table_typography":"Clean sans-serif. Percentage numbers legible. The red X on zero rows draws the eye immediately."},"supporting_objects":[],"energy":"The label tells you everything if you know what to look for.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type at very top of image above both columns","weight":"heavy/black"},"constraints":{"percentage_values_must_be_legible":true,"red_x_on_zero_percent_rows_must_be_visible_and_clear":true,"NOT_outcome_bullets_or_benefit_copy_inside_table_cells":true,"numbers_and_checkmarks_only_in_table_cells":true,"NOT_brand_name_on_either_sock":true,"dark_background_required_for_contrast":true}}',
        "negative_prompt": "outcome bullets, benefit copy inside cells, brand name, lifestyle, person wearing, face, colorful decorative elements, white background, cartoon, illustration, 3d render, collage, CTA button, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c05",
        "concept": "05 — Split Comparison Legs-Only (Reason 2: Moisture Retention)",
        "swipe_ref": "ID 011 — SCR-20260313-bjqv.jpeg (split-comparison-us-vs-them-011)",
        "reason": 2,
        "prompt": '{"style":"Clean vertical split comparison — product-forward, not person-forward. Mott & Bow aesthetic. Minimal, elevated. The socks are the subject, not the person.","lighting":"LEFT panel: cool desaturated light, flat, slightly harsh — basement or tiled bathroom. RIGHT panel: warm natural window light, slightly golden.","scene":"Hard vertical split down the centre. Both panels: same man from waist to floor — dark tailored trousers, feet on floor. NOT a full portrait. Legs and feet are the subject. LEFT panel: trouser hem slightly rumpled, sock visibly damp-looking and clinging to foot, slight discolouration at foot arch. RIGHT panel: clean trouser hem, sock sits flat and dry-looking with good structure.","primary_object":{"description":"The legs-and-feet crop in both panels — the visual comparison","left_panel_detail":"Dark trouser hem, sock that looks damp and slightly discoloured at the arch and ball of foot — the moisture failure is visible","right_panel_detail":"Clean trouser hem, sock dry and well-fitted at ankle and foot — no displacement","split_line":"Hard clean vertical divide, full image height"},"supporting_objects":[],"energy":"Same man. Different sock. Different afternoon.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type full-width above the split on a dark bar at top","weight":"heavy/black"},"constraints":{"crop_must_be_waist_to_floor_not_full_portrait":true,"moisture_indicator_visible_on_left_panel_sock":true,"NOT_man_looking_at_camera_or_posed_full_body":true,"NOT_labels_or_text_inside_either_panel":true,"NOT_brand_markings_on_socks":true}}',
        "negative_prompt": "full portrait, face visible, smiling, posed full-body fashion shot, gym, athletic, text labels inside panels, brand logo, cartoon, illustration, 3d render, collage border, badge, masthead",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c06",
        "concept": "06 — Myth-Buster Full-Bleed Person (Reason 1: Elastic Memory)",
        "swipe_ref": "ID 068 — SCR-20260313-bqut.jpeg (myth-buster-proof)",
        "reason": 1,
        "prompt": '{"style":"Full-bleed native ad — real person photo with massive bold headline overlay. The headline IS the ad. The person is the credibility context.","lighting":"Natural light, slightly gritty — outdoor urban setting or window-lit home interior. Not studio. Slight grain acceptable.","scene":"Full-bleed close-to-mid shot of a real-looking man, 40s-50s, filling most of the frame. He is NOT looking at camera — slight downward gaze, looking at something at floor level or off to the side. Background is simple: a wall, outdoor setting, or plain home environment. Massive bold headline text overlaid directly on the image — no text card, no scrim box, just white bold type sitting on the photo.","primary_object":{"description":"The massive bold headline overlay — this stops the scroll","headline_text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","headline_style":"Ultra-heavy bold white type, very large, takes up 50% of the frame. No sub-copy, no additional lines."},"supporting_objects":[],"energy":"The challenge. The pause. The rethink.","constraints":{"headline_overlay_must_be_massive_and_dominant":true,"NOT_smiling_or_looking_at_camera":true,"NOT_studio_quality_lighting":true,"person_fills_frame_as_atmosphere_not_subject":true,"headline_is_the_only_text_in_image":true,"slight_downward_gaze_required":true}}',
        "negative_prompt": "studio lighting, smiling at camera, stock photo pose, fashion model, gym, athletic, text in a card box, white background, cartoon, illustration, 3d render, badge, CTA button, person clearly centered and posed symmetrically",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c07",
        "concept": "07 — Handwritten Whiteboard Cost Math (Reason 4: Wash Sensitivity)",
        "swipe_ref": "ID 022 — SCR-20260313-bksr.jpeg (handwritten-whiteboard-price-comparison)",
        "reason": 4,
        "prompt": '{"style":"Lo-fi documentary photography — someone actually did this calculation. Not a designed graphic. Authentic imperfection.","lighting":"Warm ambient indoor light, slightly imperfect — the kind of light in a room where someone is working. Slight grain or warmth acceptable.","scene":"A real whiteboard or large notepad, photographed at a slight angle. The whiteboard has handwritten content: headline written large at top in blue or black marker, then below it a simple two-row comparison table drawn by hand. A physical rolled sock or small folded pair rests at the base or in the corner of the whiteboard frame.","primary_object":{"description":"The whiteboard surface with handwritten content","headline_on_whiteboard":"5 Reasons 100% Cotton Socks Are Designed to Fail You — written in large handwriting at top, blue or black marker","comparison_table_detail":"Hand-drawn two-row table below the headline. Row 1: label Cotton pack, 6-month replacement cycle with an approximate cost in euros (e.g. 60 per year). Row 2: label Performance Blend, 2 or more years with lower cost (e.g. 20 per year). The second row in orange or red marker — the punchline.","product_in_corner":"A small neat rolled pair of dark socks propped against the corner of the whiteboard — physical object, not drawn."},"supporting_objects":[],"energy":"The maths that changes the conversation.","constraints":{"whiteboard_must_look_real_and_photographed_not_flat_design":true,"handwriting_must_look_genuine_not_perfect_lettering":true,"cost_comparison_rows_must_be_legible":true,"orange_or_red_marker_for_performance_blend_row":true,"physical_sock_object_in_corner_required":true,"NOT_digital_screen_or_corporate_presentation_aesthetic":true}}',
        "negative_prompt": "flat design graphic, perfect typography, corporate presentation, digital screen, stock whiteboard illustration, brand logo, lifestyle, person in shot, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c08",
        "concept": "08 — Tweet-Style Peer Discovery (Reason 3: Uneven Wear)",
        "swipe_ref": "ID 007 — SCR-20260313-bilv.jpeg (fake-tweet-testimonial)",
        "reason": 3,
        "prompt": '{"style":"Social media screenshot mockup — a convincing tweet screenshot, not a designed graphic. Platform mimicry, not ad layout.","lighting":"Not applicable — flat screen simulation.","scene":"Full-frame screenshot of a tweet. Twitter/X interface. Standard layout. The tweet body is minimal — just four words. Below the tweet body: a link preview card showing the article headline as the card title and a worn sock photo as the thumbnail.","primary_object":{"description":"The tweet interface itself","tweet_chrome_detail":"Standard Twitter/X layout. Profile picture: small circular avatar, generic male headshot, slightly informal. Username: @stefan_k or similar male German first name handle. Date: Apr 2026.","tweet_body_text":"Read this. That is it. — these are the only words in the tweet body","link_preview_card_detail":"Article card at bottom of tweet. Thumbnail on left: close-up photo of a worn cotton sock showing heel damage on a hardwood floor. Card headline to the right: 5 Reasons 100% Cotton Socks Are Designed to Fail You — this is where the headline appears. Small URL text below the card headline.","engagement_row":"Reply: 3.8K. Retweet: 9.2K. Like: 41.4K. Realistic engagement numbers."},"supporting_objects":[],"energy":"Someone shared the article. 41,000 people agreed.","constraints":{"tweet_interface_must_look_authentic_not_designed":true,"headline_appears_only_in_article_link_card_not_as_separate_overlay":true,"engagement_numbers_must_be_large_and_specific":true,"tweet_body_text_must_be_minimal_four_words_only":true,"heel_damaged_sock_in_thumbnail_required":true}}',
        "negative_prompt": "brand ad layout, designed graphic, headline as separate text overlay above the tweet, empty engagement row, fake-looking interface, cartoon, illustration, 3d render, collage, badge, CTA button, masthead",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c09",
        "concept": "09 — Fabric Macro (Reason 5: Fiber Degradation)",
        "swipe_ref": "ID 083 — SCR-20260313-btab.jpeg (bathroom-mirror detail register)",
        "reason": 5,
        "prompt": '{"style":"Moody editorial macro photography — dark, detailed, slightly dramatic. Like a materials science photo or a textile lab image.","lighting":"Dramatic raking or directional light from a slight angle — emphasises texture of the weave structure, creates depth and shadow within the knit.","scene":"Extreme close-up of a cotton sock fabric surface — the knit structure of the fabric fills the entire frame. Dark coloured sock, dark background. The weave pattern is the subject. One section of the frame shows the fabric beginning to pill or thin — individual short fibers lifting from the surface. The comparison within the same frame: tight structured zone vs. beginning-to-degrade zone.","primary_object":{"description":"The fabric weave — two states side by side within the macro shot","tight_zone_detail":"Left or upper portion: individual thread paths clearly distinguishable. Weave is dense and ordered.","degrading_zone_detail":"Right or lower portion: same fabric but short fibers beginning to lift from the surface — early pilling visible. The structure is already loosening.","position":"Fills entire frame, slight angle to show depth in the weave."},"supporting_objects":[],"energy":"What cotton does to itself after twenty washes.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type overlaid top portion of image, large, against the dark fabric background — naturally high contrast","weight":"heavy/black"},"constraints":{"macro_fabric_shot_fills_entire_frame":true,"pilling_or_fiber_degradation_visible_in_one_zone":true,"NOT_product_packaging_visible":true,"dark_colour_sock_required_for_headline_contrast":true,"weave_structure_clearly_distinguishable_in_tight_zone":true}}',
        "negative_prompt": "clean undamaged fabric only, product packaging, brand name, full sock visible, person, lifestyle, bright light background, colorful sock, cartoon, illustration, 3d render, collage, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c10",
        "concept": "10 — Pattern Interrupt Paradox Typographic (Reason 2: Moisture)",
        "swipe_ref": "ID 076 — SCR-20260313-bsht.jpeg (pattern-interrupt-paradox)",
        "reason": 2,
        "prompt": '{"style":"Clean typographic pattern interrupt — the claim is designed to create a double-take. Minimal editorial. The dissonance between the alarming headline and the calm product is the entire ad.","lighting":"Not applicable — flat background. Product: clean even light.","scene":"Mint green or warm cream background — unexpected for a sock ad. Headline at top large and dominant. Small clean product image at the bottom: a neat rolled or folded pair of dark socks, clean, structured. The calm product sitting under the alarming claim is intentional.","primary_object":{"description":"The headline text dominates — the product is deliberately small","headline_detail":"Bold heavy sans-serif. Very large — approximately 60-65% of the vertical frame. Text: 5 Reasons 100% Cotton Socks Are Designed to Fail You. White or very dark type on the soft background — strong contrast. No sub-copy.","product_detail":"Small neat product visual at bottom — a rolled or folded pair of dark structured socks. Clean, professional-looking. Approximately 20% of vertical frame height. No brand name.","background_colour":"Mint green or warm cream — deliberately soft and unexpected"},"supporting_objects":[],"energy":"The calm product sitting below the alarming claim.","constraints":{"headline_must_dominate_composition_at_least_60_percent_of_frame":true,"product_must_be_small_and_subordinate":true,"NOT_bright_saturated_or_white_background":true,"NOT_brand_name_on_product":true,"background_must_be_mint_green_or_warm_cream_not_white":true}}',
        "negative_prompt": "white background, dark background, bright saturated color, brand name, lifestyle, person, face, cartoon, illustration, 3d render, badge, CTA button, sub-copy text, busy composition, black background",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c11",
        "concept": "11 — Lower Body Shot 2PM Problem (Reason 1: Elastic Memory)",
        "swipe_ref": "ID 116 — SCR-20260313-bvmm.jpeg (native-advertorial-116, editorial magazine register)",
        "reason": 1,
        "prompt": '{"style":"Editorial documentary tight crop — feels like a detail shot from a longer investigative piece. Not a product photo.","lighting":"Natural indoor light — hallway, entrance, or office. Neutral warm tones. Practical environment.","scene":"Tight crop of male lower body — from roughly mid-thigh to floor. Dark smart-casual trousers, leather shoes, and a sock visible at the trouser hem. The sock shows the elastic memory failure in progress: cuff has slipped down to reveal a gap between cuff and shoe at one side. The detail is the point — this is 2pm, mid-afternoon, third time pulling it up.","primary_object":{"description":"Lower body only — dark trousers, leather shoes, sock at hem showing the problem","sock_detail":"Grey or dark navy sock. The cuff has slipped — visibly lower on one ankle than the other, or the cuff is loose enough that it is gathered rather than sitting flat. No dramatic hole — the drift is the problem.","position":"Trouser hem and leather shoe in frame, shot at slight downward angle. The sock displacement is the key visual."},"supporting_objects":[],"energy":"Two PM. He has reached down for the third time today.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type dominant in upper portion of image, large, full width","weight":"heavy/black"},"constraints":{"NOT_above_mid_thigh":true,"sock_cuff_slippage_must_be_visible_at_hem":true,"NOT_athletic_or_casual_shoes_must_be_leather_or_smart":true,"NOT_brand_name_on_sock_or_shoes":true,"sock_drift_or_cuff_displacement_is_the_key_detail":true}}',
        "negative_prompt": "face, torso above mid-thigh, athletic shoes, sneakers, gym, sportswear, clean perfectly-fitted sock, brand name, colorful sock, cartoon, illustration, 3d render, badge, callout labels",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c12",
        "concept": "12 — Us-Vs-Them Comparison (Reason 4: Wash Sensitivity)",
        "swipe_ref": "ID 025 — SCR-20260313-blgb.jpeg (us-vs-them-comparison-025)",
        "reason": 4,
        "prompt": '{"style":"Clean editorial product comparison — two-column us-vs-them format. Dark background. Minimal, evidence-based, not salesy.","lighting":"Not applicable — dark background with clean product photography.","scene":"Dark charcoal background. Two columns side by side. Left column: 100% cotton sock with a laundry-fail visual (shrunken or misshapen after hot wash, colour faded). Red X marks against each failure. Right column: blend sock, neat and structured, same wash. Green checkmarks against each point. Headline at top spanning both columns.","primary_object":{"description":"Two-column comparison layout","left_column_cotton_detail":"Cotton sock shown post-wash — visibly shrunken or misshapen, colour slightly faded or washed out. Three failure points with red X: Cold water only | Air dry only | Do not tumble dry","right_column_blend_detail":"Blend sock post-wash — maintains shape and colour. Three points with green check: Any temperature | Tumble dry fine | In with your jeans","column_headers":"LEFT: 100% Cotton (plain) | RIGHT: 78/20 Blend (teal accent)"},"supporting_objects":[],"energy":"The care label is the product admitting what it cannot handle.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type at very top spanning both columns","weight":"heavy/black"},"constraints":{"red_x_items_must_be_legible_on_left":true,"green_check_items_must_be_legible_on_right":true,"NOT_brand_name_on_either_sock":true,"NOT_price_in_image":true,"dark_background_required":true,"care_instruction_points_must_be_the_comparison_not_performance_claims":true}}',
        "negative_prompt": "brand name, price, lifestyle photo, person wearing, face, colorful background, white background, cartoon, illustration, 3d render, badge, CTA button, performance specs as comparison points",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c13",
        "concept": "13 — Outdoor UGC Full-Bleed Person (Reason 2: Moisture)",
        "swipe_ref": "ID 052 — SCR-20260313-bohi.jpeg (shock-reframe)",
        "reason": 2,
        "prompt": '{"style":"Full-bleed UGC-style outdoor photo with large bold headline overlay. Real person, real environment, massive typography. Shot-by-a-friend energy, not a brand shoot.","lighting":"Bright natural outdoor light — city pavement, park, or open urban space. Slightly overexposed is fine. Real light, not colour-corrected.","scene":"Full-bleed photo of a real-looking man outdoors, slightly off-angle — maybe shot from below or from a candid side angle. He fills most of the frame. Outdoors behind him: trees, pavement, building edge. Not posed — slightly in motion or looking at something off-camera. Large bold headline text directly on the photo — no card, no scrim box, no semi-transparent overlay box.","primary_object":{"description":"The bold headline — the scroll-stop","headline_text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","headline_style":"Ultra-bold white, very large, stacked across lower half of the photo directly on the image. Headline only — no other copy."},"supporting_objects":[],"energy":"The challenge tossed out loud. He looks like he already found the answer.","constraints":{"NOT_studio_or_professional_outdoor_shoot":true,"headline_directly_on_photo_no_card_no_scrim_box":true,"headline_is_the_only_text_in_image":true,"person_is_atmosphere_not_subject_headline_is_scroll_stop":true,"NOT_smiling_or_looking_at_camera":true,"outdoor_setting_with_practical_environment_required":true}}',
        "negative_prompt": "studio lighting, posed fashion shoot, smiling at camera, gym, athletic wear, text in a card box, white background, cartoon, illustration, 3d render, badge, CTA button, stock photo composition",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c14",
        "concept": "14 — Seminar Authority (Reason 3: Uneven Wear)",
        "swipe_ref": "ID 298 — fb57375a-8f20-4747-80a9-a713b24b832b.jpeg (seminar-presentation-authority)",
        "reason": 3,
        "prompt": '{"style":"Documentary event photography — candid shot at a professional workshop or seminar. Not staged. The argument is on the screen.","lighting":"Mixed indoor event lighting — ambient room light plus projected screen light. Warm. Practical meeting room or small conference space, not a stage with spotlights.","scene":"A professional workshop room. Expert — male, 45-55, practical clothing (dark shirt, not a formal suit) — standing beside a projector screen, arm extended pointing at it. The screen shows the headline text in large bold type. Audience: backs and tops of heads of 4-6 seated people in the foreground, slightly out of focus, attention directed toward the presenter and screen.","primary_object":{"description":"The presenter and projector screen together — the argument is on the screen, the presenter is pointing at it","presenter_detail":"Male 45-55. Dark shirt or casual jacket. Standing posture, arm extended pointing at screen. Expression: making a point, engaged. NOT looking at camera.","screen_text_detail":"Projector screen shows headline in bold black type on white or cream: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Text fills most of the screen and is legible.","audience_detail":"Backs of 4-6 seated attendees in foreground, slightly out of focus. Workshop or small conference context."},"supporting_objects":[],"energy":"The room is paying attention. He has the evidence.","constraints":{"screen_text_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","presenter_must_be_pointing_at_screen_not_at_camera":true,"audience_backs_in_foreground_required":true,"NOT_classroom_or_school_setting":true,"NOT_other_text_visible_on_walls_or_elsewhere_in_room":true,"headline_on_screen_is_the_only_text_in_image":true}}',
        "negative_prompt": "classroom, school, looking at camera, other text on walls or posters, brand logo, colorful presentation graphics, cartoon, illustration, 3d render, badge, separate text overlay outside the screen, sub-copy",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c15",
        "concept": "15 — Shock Reframe Text-Only (Reason 5: Fiber Degradation)",
        "swipe_ref": "ID 010 — SCR-20260313-bjfz.png (anti-design-text-only)",
        "reason": 5,
        "prompt": '{"style":"Anti-design text-only — pure typography on a solid background. No images. The words are the entire ad. Resembles a tweet screenshot or a bold editorial statement, not an advertisement.","lighting":"Not applicable — flat solid background.","scene":"Solid dark background (near-black or very dark charcoal). Single large bold white headline text centred in frame. Nothing else — no images, no product, no decorative elements, no sub-copy. The typographic weight is the entire scroll-stop.","primary_object":{"description":"The headline text itself","headline_detail":"Heavy bold white sans-serif or slab-serif. Very large — takes up most of the vertical frame. Text: 5 Reasons 100% Cotton Socks Are Designed to Fail You. The size and weight do the work. No sub-heading, no author, no badge.","position":"Centred, with significant breathing room on all sides."},"supporting_objects":[],"energy":"The authority of a statement that does not need context.","constraints":{"text_content_must_be_exact":"5 Reasons 100% Cotton Socks Are Designed to Fail You","NOT_any_other_text_elements_present":true,"dark_background_required":true,"NOT_a_designed_graphic_with_decorative_elements":true,"must_look_like_bold_editorial_statement_not_ad":true}}',
        "negative_prompt": "colorful background, white background, decorative elements, sub-headline, author byline, product image, badge, border, graphic design flourishes, cartoon, illustration, 3d render, collage, person, lifestyle",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c16",
        "concept": "16 — Problem-Agitate Lifestyle (Reason 1: Elastic Memory)",
        "swipe_ref": "ID 045 — SCR-20260313-bnre.jpeg (problem-agitate-lifestyle)",
        "reason": 1,
        "prompt": '{"style":"Native advertorial lifestyle — real person photo with bold editorial headline overlay. The scene shows the moment of the problem. The headline names the cause.","lighting":"Natural indoor light — office environment, practical space. Slightly warm. Nothing studio.","scene":"Mid-shot of a man in smart-casual work clothes — he is bent slightly forward, reaching down to pull up his sock at the ankle. The gesture is entirely natural: the sock has slipped and he is correcting it. He is NOT looking at camera. Office or practical indoor background behind him — desk, hallway, or window. Bold headline text overlaid in upper portion of the image.","primary_object":{"description":"The man mid-gesture of pulling up his sock — the problem in action","gesture_detail":"Bent slightly forward or at the waist, one hand at ankle pulling cuff upward. Natural, habitual, slightly resigned gesture. This is not the first time today.","clothing_detail":"Dark smart-casual trousers, plain shirt or casual jacket. Not gym wear.","background_detail":"Office or home corridor behind him — slightly out of focus."},"supporting_objects":[],"energy":"The unconscious daily ritual. He does this four times a day without thinking about it.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white type in upper portion of image, large","weight":"heavy/black"},"constraints":{"man_must_be_in_act_of_pulling_up_sock_at_ankle":true,"NOT_posed_or_looking_at_camera":true,"NOT_gym_or_athletic_context":true,"gesture_must_look_habitual_not_performed":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "looking at camera, smiling, posed portrait, gym, athletic wear, studio lighting, fashion model, text in card box, cartoon, illustration, 3d render, badge, CTA button, dramatic expression",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c17",
        "concept": "17 — Star Rating Product Comparison (Reason 3: Uneven Wear)",
        "swipe_ref": "ID 103 — SCR-20260313-bubh.png (side-by-side-comparison)",
        "reason": 3,
        "prompt": '{"style":"Clean editorial product comparison photography — two products, one outcome difference. Cream background. Star ratings. Minimal.","lighting":"Even soft diffused light, cream or off-white background, no harsh shadows.","scene":"Two sock products side by side on a clean cream surface. Left: neat rolled pair in good condition — structured, no visible wear. Star rating below: five gold stars. Right: single cotton sock laid flat showing visible heel damage — worn-through or thinning patch at heel. Star rating below: two gold stars.","primary_object":{"description":"Two sock conditions on cream background for direct visual comparison","left_sock_detail":"Neatly rolled or folded dark sock pair — structured, retains shape, no wear. Five gold star row below. No brand name.","right_sock_detail":"Single cotton sock laid flat — heel clearly thinner, visible worn patch or hole. Two gold stars, three grey stars below. No brand name.","star_rating_detail":"Stars as simple graphic row below each sock. Left: 5 gold. Right: 2 gold, 3 grey. No review text, no quote, just star rows."},"supporting_objects":[],"energy":"Same category. Very different six months in.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold black type on white strip at very top of image spanning both products","weight":"heavy/black"},"constraints":{"star_ratings_must_be_visible_and_correctly_differentiated":"5 left, 2 right","heel_damage_on_right_sock_must_be_clear_focal_point":true,"NOT_review_text_or_quote_in_image":true,"NOT_brand_name_on_either_sock":true,"cream_or_off_white_background_required":true,"NOT_person_wearing_socks":true}}',
        "negative_prompt": "brand name, review text quote, person wearing, face, gym, studio product shot on stark white, colorful socks, athletic socks, cartoon, illustration, 3d render, badge, CTA button, sub-copy",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c18",
        "concept": "18 — Native News Article Layout (Reason 4: Wash Sensitivity)",
        "swipe_ref": "ID 305 — d9375446-1c53-4708-bfab-59a213fd7b13.jpeg (native-news-advertorial)",
        "reason": 4,
        "prompt": '{"style":"News article screenshot — resembles a quality editorial publication layout. The visual design communicates authority, not advertising.","lighting":"Not applicable for text sections. Editorial photo: natural indoor light.","scene":"Full news article layout. White or very light grey background for text sections. Bold large headline text dominant at top. Below it: an editorial photograph of a worn cotton sock that has shrunk or misshapen after washing — sitting on a laundry surface or wooden floor. Small date stamp. The composition reads as a genuine consumer news article.","primary_object":{"description":"The news article layout itself","headline_section_detail":"Bold heavy black type on white. Text: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Headline is large, takes up top third.","photo_detail":"Below headline: editorial photo — shrunken or misshapen cotton sock on laundry surface or floor after washing. Natural light. Looks like a photo editor would have chosen it for a consumer watchdog piece.","date_stamp_detail":"Small grey text: April 2026. Minimal — one line. Looks like a real date stamp."},"supporting_objects":[],"energy":"This was reported. This is documented.","constraints":{"must_look_like_genuine_consumer_news_article_not_ad":true,"NOT_sub_deck_or_author_byline_in_image":true,"NOT_learn_more_button_in_image":true,"sock_damage_or_shrinkage_visible_in_editorial_photo":true,"date_stamp_must_be_small_and_grey_not_prominent":true}}',
        "negative_prompt": "advertisement layout, Learn More button, sub-deck text, author byline, publication logo, colorful graphic elements, cartoon, illustration, 3d render, collage, badge, clean undamaged sock, bright saturated background",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c19",
        "concept": "19 — Protest Sign Street Portrait (Reason 5: Fiber Degradation)",
        "swipe_ref": "ID 299 — 045465c8-0a0f-48b8-953c-248115b625ab.jpeg (protest-sign-street-portrait)",
        "reason": 5,
        "prompt": '{"style":"Street portrait editorial — person holds handwritten sign. Documentary register. Raw, unpolished, feels like a real moment captured.","lighting":"Natural outdoor or window-adjacent indoor light. Slightly overcast or diffused. Not corrected.","scene":"Man, 40s-50s, holding up a handwritten cardboard sign or large piece of paper. The sign text is handwritten, large, fills most of the sign surface. He is NOT looking at camera — eyes on the sign or cast down. The background is simple: a wall, building exterior, or plain indoor setting. Not posed for a camera.","primary_object":{"description":"The handwritten sign is the focal point — the man is the credibility","sign_detail":"Cardboard or large paper. Handwritten in thick black marker or pen: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Large enough to read clearly. The handwriting looks real — slightly irregular, not typeset.","person_detail":"Male 40s-50s. Practical casual clothing. Holding sign at chest or above — slightly raised. Expression neutral or slightly serious. NOT smiling."},"supporting_objects":[],"energy":"Someone cared enough to write this down and hold it up.","constraints":{"sign_text_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","handwriting_on_sign_must_look_genuine_not_typeset":true,"NOT_looking_at_camera_or_smiling":true,"sign_is_the_primary_visual_object":true,"headline_appears_only_on_the_handwritten_sign_no_separate_overlay":true}}',
        "negative_prompt": "looking at camera, smiling, studio lighting, professional portrait, stock photo pose, gym, athletic, fashion, typeset text on sign, digital display, cartoon, illustration, 3d render, badge, separate text overlay",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c20",
        "concept": "20 — Founder Letter Social Post",
        "swipe_ref": "ID 005 — SCR-20260313-biiu.png (founder-letter-social-post)",
        "prompt": '{"style":"Instagram or Facebook sponsored post — founder letter format. Clean, personal, editorial. Resembles a handwritten note shared as a social post, not a display ad.","lighting":"Not applicable — clean off-white or very light cream background.","scene":"Clean light background. A handwritten-style or clean note card layout. At the top: the headline as the opening statement of the note, in large handwriting or printed block text. Below it: three short bullet lines in smaller handwriting (not the headline — these are not part of the image text, they are visual texture suggesting a list is there). At the bottom: a simple drawn or stamped signature initial.","primary_object":{"description":"The note card composition — intimate and editorial","top_headline_detail":"The note opens with: 5 Reasons 100% Cotton Socks Are Designed to Fail You — this is the headline, rendered in large handwriting or clean printed block text, as the opening line of the note card. This is the ONLY legible text in the image.","bullet_lines_below_detail":"Three short horizontal lines below the headline — these suggest bullet list items exist but the text is too small or smudged to read. They are visual rhythm, not copy.","signature_detail":"Simple initial or small X at the bottom of the note — no name, no attribution.","background":"Off-white or very light cream — soft, not stark white"},"supporting_objects":[],"energy":"A note someone left themselves. The claim is the opening.","constraints":{"headline_at_top_of_note_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","bullet_lines_below_must_be_too_small_or_indistinct_to_read":true,"NOT_full_body_copy_visible_in_image":true,"NOT_CTA_button_or_learn_more":true,"note_card_format_must_look_personal_not_corporate":true,"headline_is_the_only_legible_text":true}}',
        "negative_prompt": "corporate design, CTA button, Learn More, body copy legible, brand logo, product image, colorful background, dark background, cartoon, illustration, 3d render, badge, masthead, formal layout",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c21",
        "concept": "21 — Laundry Basket Discovery",
        "swipe_ref": "ID 062 — SCR-20260313-bqhj.jpeg (native-advertorial)",
        "prompt": '{"style":"Documentary close-up photography — candid domestic moment. Feels like someone noticed something they had been ignoring for months.","lighting":"Warm ambient indoor light — laundry room or bathroom, practical and unglamorous. Slightly warm yellow tones.","scene":"A laundry basket or pile of clean laundry on a surface. One dark cotton sock is pulled to the front of the pile, held up slightly — showing a visible hole at the heel or toe. The rest of the laundry is blurred background. The sock is the focal point. Bold headline text overlaid across the upper portion.","primary_object":{"description":"The worn sock emerging from the laundry pile","sock_detail":"Dark navy or grey cotton sock. Clear hole or heavily worn patch at heel or toe. Held or positioned so the damage faces the viewer directly.","background_detail":"Rest of laundry pile blurred behind — shirts, other items. Domestic, lived-in."},"supporting_objects":[],"energy":"Found it in the wash. Not the first one this month.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type upper portion, full width","weight":"heavy/black"},"constraints":{"sock_damage_must_be_the_clear_focal_point":true,"NOT_product_packaging_visible":true,"NOT_studio_shot":true,"laundry_context_required_in_background":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "clean sock, studio shot, white background, product packaging, brand name, person wearing, face, gym, athletic, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c22",
        "concept": "22 — Coffee Table Flat Lay Editorial",
        "swipe_ref": "ID 053 — SCR-20260313-bomg.png (ingredient-comparison)",
        "prompt": '{"style":"Overhead flat lay — editorial product photography. Cold, analytical. Resembles a consumer product investigation shoot.","lighting":"Even overhead natural light — cool, diffused. No shadows. Cream or stone surface.","scene":"Overhead shot of a flat lay on a stone or cream surface. Centre: a single dark cotton sock laid flat, showing clear visible heel damage. To the left: a small sticky note with the headline written in pen — this is the only text. No other objects. Minimal, clinical.","primary_object":{"description":"The sock and the sticky note — together they make the argument","sock_detail":"Dark sock laid flat, heel zone showing thinning fabric or small hole. The damage is clearly visible and centred in frame.","sticky_note_detail":"Small yellow or white sticky note to the left of the sock. Handwritten pen: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Handwriting looks real, slightly informal.","surface_detail":"Stone, slate, or cream surface — practical editorial surface, not a styled photo."},"supporting_objects":[],"energy":"The evidence laid out flat. Clinical and undeniable.","constraints":{"sock_damage_must_be_visible_and_centred":true,"sticky_note_text_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","headline_appears_only_on_sticky_note_no_separate_overlay":true,"NOT_brand_name_on_sock":true,"overhead_shot_required":true,"NOT_colourful_or_busy_surface":true}}',
        "negative_prompt": "brand name, overhead studio shot with stark white, colourful surface, multiple props, person, face, lifestyle, cartoon, illustration, 3d render, badge, text overlay separate from sticky note",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c23",
        "concept": "23 — Drawer Full of Dead Socks",
        "swipe_ref": "ID 076 — SCR-20260313-bsht.jpeg (pattern-interrupt-paradox)",
        "prompt": '{"style":"Documentary close-up — the evidence is accumulated, not isolated. This is a pattern, not a single incident.","lighting":"Warm indoor ambient — bedroom or hallway drawer, slightly warm and practical.","scene":"An open sock drawer photographed from slightly above. The drawer contains 6-8 pairs of cotton socks in various states of wear — some visibly pilled, one with a heel worn through, a few misshapen from washing. Not all are destroyed — but the overall impression is a drawer full of socks that are degrading. Bold headline overlaid at top.","primary_object":{"description":"The open drawer as accumulated evidence","drawer_contents_detail":"Mix of dark and grey cotton socks in different wear states — pilled surfaces, one with visible heel hole, a few pairs where the elastic cuff is loose and slack. Practical drawer environment, slightly messy.","pattern_detail":"The accumulation is the point — this is not one bad sock, this is a category failure."},"supporting_objects":[],"energy":"Every man has this drawer. He just has not named it yet.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at very top of image","weight":"heavy/black"},"constraints":{"drawer_must_contain_multiple_socks_in_different_wear_states":true,"at_least_one_sock_with_visible_damage_required":true,"NOT_neat_organised_drawer_with_perfect_socks":true,"NOT_brand_markings_on_any_sock":true,"practical_domestic_setting_required":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "neat organised drawer, perfect clean socks, brand name, studio shot, white background, person, face, athletic socks, colourful socks, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c24",
        "concept": "24 — Man Reading — UGC Over-Shoulder",
        "swipe_ref": "ID 071 — SCR-20260313-brbu.jpeg (testimonial-discovery)",
        "prompt": '{"style":"Over-shoulder UGC — someone photographed this person reading something that changed their perspective. Phone camera, natural, imperfect.","lighting":"Warm desk lamp or window light from the side — reading environment. Not bright, not studio.","scene":"Over-shoulder shot of a man seated at a desk or table — he is reading something on a laptop or holding printed pages. We see the back of his head and shoulders, his posture slightly forward as someone engaged with what they are reading. The laptop screen or paper content is NOT legible. Bold headline overlaid in upper portion of the image.","primary_object":{"description":"The man absorbed in reading — the posture of discovery","posture_detail":"Leaning slightly forward, engaged. Right or left shoulder slightly raised. The posture of someone who has just read something they did not expect.","device_detail":"Laptop on desk or printed paper in hand. Screen content blurred or not legible — we do not need to see what he is reading.","background_detail":"Desk surface, wall behind, window or bookshelf — practical home or office environment."},"supporting_objects":[],"energy":"He is reading it right now. His posture says it landed.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type upper portion, large","weight":"heavy/black"},"constraints":{"NOT_looking_at_camera":true,"over_shoulder_shot_required_face_not_visible_or_partially_visible":true,"reading_posture_must_look_engaged_and_absorbed":true,"screen_or_page_content_must_NOT_be_legible":true,"practical_desk_or_reading_environment_required":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "looking at camera, smiling, studio, stock photo pose, phone in hand taking selfie, athletic, gym, face clearly visible and centred, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c25",
        "concept": "25 — Bold Typographic Dark Card",
        "swipe_ref": "ID 010 — SCR-20260313-bjfz.png (anti-design-text-only)",
        "prompt": '{"style":"Anti-design typographic statement — dark card, single claim, no imagery. Resembles a quote card shared between professionals, not a brand advertisement.","lighting":"Not applicable — flat dark background.","scene":"Very dark background — near black or deep charcoal. A clean white rounded-corner card centred in the frame, with significant dark border around it. Inside the card: the headline in large bold black type only. The card is the entire composition. Nothing else.","primary_object":{"description":"The white card on dark background","card_detail":"White or very light grey card. Rounded corners. Bold black heavy sans-serif headline: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Headline takes up most of the card interior. No sub-text, no author, no badge.","dark_border_detail":"Generous dark space around all card edges — the card floats in the dark background."},"supporting_objects":[],"energy":"The kind of thing someone screenshots and sends without comment.","constraints":{"white_card_must_float_on_dark_background_with_generous_border":true,"headline_is_the_only_text_on_card":true,"NOT_any_decorative_elements_on_card":true,"rounded_corners_on_card_required":true,"headline_content_exact":"5 Reasons 100% Cotton Socks Are Designed to Fail You"}}',
        "negative_prompt": "colourful background, gradient, decorative elements, sub-text, author name, badge, brand logo, product image, person, lifestyle, cartoon, illustration, 3d render, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c26",
        "concept": "26 — Commuter Legs Street Candid",
        "swipe_ref": "ID 011 — SCR-20260313-bjqv.jpeg (split-comparison)",
        "prompt": '{"style":"Street documentary lower-body crop — candid commuter photography. The person is anonymous; the sock is the detail.","lighting":"Natural outdoor urban light — overcast or morning city light. Slightly cool. Pavement or platform surface visible.","scene":"Tight crop of commuter lower body on an urban surface — pavement, train platform, or office building steps. Dark smart trousers, leather shoes. The sock at the trouser hem is visible and shows a cuff that has slipped slightly down. The environment behind is blurred urban background. Bold headline overlaid at top.","primary_object":{"description":"Lower body crop — the problem detail is at the hem","sock_at_hem_detail":"Grey or dark sock with cuff slipped slightly — not sitting flush with the trouser hem. A small gap or slack cuff visible at one ankle.","environment_detail":"Urban pavement or stone steps. Blurred commuter environment behind. Practical and real.","crop":"Waist to floor maximum — no face, no torso above mid-thigh."},"supporting_objects":[],"energy":"Every commute. Every time he reaches the office and realises it has happened again.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top, full width","weight":"heavy/black"},"constraints":{"crop_must_be_waist_to_floor_no_face":true,"urban_commuter_environment_required":true,"sock_cuff_slippage_visible_at_hem":true,"NOT_athletic_shoes_must_be_leather_or_smart":true,"NOT_brand_name_on_sock_or_shoes":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "face visible, full portrait, smiling, gym, athletic shoes, sneakers, sportswear, clean perfect sock, brand name, studio, white background, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c27",
        "concept": "27 — Newspaper Cutout Style",
        "swipe_ref": "ID 022 — SCR-20260313-bksr.jpeg (handwritten-whiteboard)",
        "prompt": '{"style":"Collage cutout editorial — newspaper clippings assembled into a flat lay. Looks like someone built this from real articles, not designed it.","lighting":"Even overhead natural light — cream or newspaper-yellow surface, authentic paper texture.","scene":"Overhead flat lay on a cream or slightly yellowed paper surface. Multiple cut newspaper or magazine fragments arranged around a central bold headline. The central element is a large cut strip of newsprint with the headline printed in bold newspaper type. Surrounding it: 3-4 smaller cut fragments showing torn paper edges — no legible text on the fragments, just torn paper texture. One small dark sock sits at the corner as a physical object.","primary_object":{"description":"The central headline newsprint strip and surrounding torn paper fragments","central_headline_strip_detail":"Cut strip of newspaper-textured paper. Bold black serif headline type: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Torn edges on the strip.","fragment_detail":"3-4 smaller torn fragments around the centre. Paper texture visible, no legible text on them.","sock_object_detail":"Small dark rolled sock at one corner — physical object, not cut paper."},"supporting_objects":[],"energy":"Someone assembled the evidence.","constraints":{"central_headline_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","surrounding_fragments_must_NOT_contain_legible_text":true,"torn_paper_edges_required_on_headline_strip":true,"NOT_digital_or_designed_graphic_look":true,"overhead_shot_required":true,"headline_is_the_only_legible_text_in_image":true}}',
        "negative_prompt": "digital graphic design look, clean laser-cut edges, brand logo, other legible text in fragments, person, face, colourful background, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c28",
        "concept": "28 — Window Reflection — Man Getting Dressed",
        "swipe_ref": "ID 116 — SCR-20260313-bvmm.jpeg (native-advertorial editorial register)",
        "prompt": '{"style":"Moody editorial documentary — window reflection or mirror glimpse. Private moment, not performed for a camera.","lighting":"Soft morning window light — slightly cool, directional. The kind of light before the workday starts. Some lens flare or window glare acceptable.","scene":"A man seen partially through a window reflection or in a hall mirror — he is in the act of pulling on or adjusting his trousers at the ankle, which means the sock is visible at the hem. Not looking at the camera or the mirror — absorbed in the task. The scene has the quality of being caught unobserved. Bold headline overlaid across the lower portion.","primary_object":{"description":"The reflected or mirror glimpse — private morning moment","reflection_detail":"Window glass or mirror showing the man at waist-to-floor level, adjusting trouser hem or sock. The reflection has slight distortion or light interference — it looks real, not staged.","sock_at_hem_detail":"Sock visible at trouser hem as he adjusts — the domestic detail is the context for the headline."},"supporting_objects":[],"energy":"The morning routine. He does this without thinking about why.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type lower portion, large","weight":"heavy/black"},"constraints":{"reflection_or_mirror_glimpse_register_required":true,"NOT_looking_at_camera_or_mirror":true,"NOT_studio_or_posed_portrait":true,"morning_getting_dressed_context_required":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "looking at camera, smiling, studio lighting, posed fashion shoot, athletic wear, gym, face centred and prominent, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c29",
        "concept": "29 — Torn Packaging Label Macro",
        "swipe_ref": "ID 083 — SCR-20260313-btab.jpeg (detail-shot register)",
        "prompt": '{"style":"Macro product detail photography — editorial and slightly confrontational. The packaging label is the evidence.","lighting":"Raking directional light from side — emphasises texture of paper and print. Slightly warm.","scene":"Extreme close-up of a care label or packaging label from a cotton sock — the fabric tag or small paper insert that says 100% Cotton. The label fills most of the frame. The material percentage is legible. Below it or on top of it, a large bold headline overlay.","primary_object":{"description":"The 100% Cotton label — the villain named in its own words","label_detail":"Fabric care label or paper packaging insert. Text reads 100% Cotton clearly legible. Torn at one edge — as if it was pulled from a product. The label sits on a dark surface or is held against a textured background.","label_typography":"Standard care label font — the ordinary mundane thing that turns out to be the entire problem."},"supporting_objects":[],"energy":"The answer was on the label the whole time.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type overlaid above or below the label","weight":"heavy/black"},"constraints":{"100_percent_cotton_text_on_label_must_be_legible":true,"label_must_look_real_not_digitally_designed":true,"dark_or_textured_background_required_for_contrast":true,"NOT_brand_name_on_label":true,"torn_or_worn_label_edges_preferred":true,"headline_is_the_only_additional_text_in_image":true}}',
        "negative_prompt": "brand name on label, clean white background, digital mockup, illustrated label, colourful packaging, person wearing, face, athletic, gym, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c30",
        "concept": "30 — Microscope Lab Fabric Shot",
        "swipe_ref": "ID 298 — fb57375a-8f20-4747-80a9-a713b24b832b.jpeg (authority register)",
        "prompt": '{"style":"Scientific documentary photography — fabric under magnification. Clinical, authoritative, investigative.","lighting":"Clinical bright even light with slight cool tones — lab or research environment. The fabric texture is the subject.","scene":"A cotton sock fabric sample on a clinical surface, appearing as if photographed under a magnifying lens or macro lab setup. The weave structure is visible in high detail. Short individual cotton fibres are clearly distinguishable — some beginning to fray or lift at the surface. A ruled measuring line or scale marker is visible at one edge of the frame as a documentary detail. Bold headline overlaid across the top.","primary_object":{"description":"The cotton fabric sample under clinical examination","weave_detail":"Individual cotton yarns clearly visible — irregular fibre length, short fibres beginning to lift from the weave surface. The structural imperfection of uncombed cotton fibres is the focal point.","scale_marker_detail":"Small ruler or measurement indicator at frame edge — the clinical detail that says this is documented, not just observed."},"supporting_objects":[],"energy":"This is what the material looks like when you actually look.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top on dark area or overlay","weight":"heavy/black"},"constraints":{"fabric_weave_and_fibre_detail_must_be_the_subject":true,"scale_marker_or_ruler_visible_at_frame_edge":true,"clinical_lab_register_required":true,"NOT_product_packaging_visible":true,"NOT_lifestyle_or_person_in_shot":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "brand name, person, lifestyle, fashion, product packaging, colourful background, cartoon, illustration, 3d render, badge, CTA button, microscope visible in shot",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c31",
        "concept": "31 — Phone Screenshot Saved Article",
        "swipe_ref": "ID 007 — SCR-20260313-bilv.jpeg (social screenshot register)",
        "prompt": '{"style":"Phone screenshot — someone saved this article to read later. Platform mimicry. The frame is the phone itself.","lighting":"Not applicable — screen simulation.","scene":"A phone screen showing a saved article or browser bookmark. The article title is the headline in large bold type at the top of the screen. Below the headline: a small editorial photo thumbnail — a close-up of a worn dark cotton sock on a hardwood floor. The URL bar at the top of the browser shows a generic consumer-guide style URL. Below the article thumbnail: a small save or bookmark indicator. The phone chrome is visible — the frame is a real phone.","primary_object":{"description":"The phone screen showing the saved article","browser_bar_detail":"Generic URL — something like consumer-guide.eu or socktest.at — not a brand URL. Small and grey, not prominent.","article_headline_detail":"Bold black type on white browser background: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Large and dominant on screen.","thumbnail_detail":"Small rectangular editorial photo below headline — close-up of worn dark sock, heel damage visible, on hardwood floor.","save_indicator":"Small bookmark or saved icon — the person meant to come back to this."},"supporting_objects":[],"energy":"He saved it. He knows he needs to read it.","constraints":{"phone_chrome_visible_as_frame":true,"headline_on_screen_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","NOT_brand_URL_in_browser_bar":true,"worn_sock_thumbnail_required":true,"headline_is_the_only_prominent_text_on_screen":true}}',
        "negative_prompt": "brand URL, brand name in header, lifestyle, person not holding phone, full desktop browser, cartoon, illustration, 3d render, badge, CTA button, other article headlines visible",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c32",
        "concept": "32 — Two Socks Ageing Comparison Macro",
        "swipe_ref": "ID 025 — SCR-20260313-blgb.jpeg (us-vs-them-comparison)",
        "prompt": '{"style":"Clean editorial product photography — two objects, one contrast. The objects tell the story without labels.","lighting":"Soft even natural light from above — cream or stone surface. No harsh shadows. The texture difference is the subject.","scene":"Two dark socks laid flat side by side on a cream or stone surface. Left sock: structure maintained, weave clean and tight. Right sock: same age indicated by identical colour but the heel zone shows clear degradation — pilling, thinning, or a small worn patch. No labels, no text between them. Bold headline overlaid at the bottom of the image as the only text.","primary_object":{"description":"Two socks — same material, different condition","left_sock_detail":"Dark navy or charcoal sock. Flat and structured. Weave intact. Clean heel zone.","right_sock_detail":"Same colour dark sock. Visible pilling on surface, heel zone thinned or beginning to fail. Not dramatically destroyed — just clearly past its best.","comparison_surface":"Cream or stone surface. No props, no labels, no text between them — the visual contrast is the argument."},"supporting_objects":[],"energy":"Same laundry. Same age. One question.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type across the bottom, full width, against the surface","weight":"heavy/black"},"constraints":{"both_socks_must_be_same_colour_to_make_condition_contrast_legible":true,"NOT_any_labels_between_socks":true,"NOT_brand_name_on_either_sock":true,"damage_on_right_sock_must_be_visible_but_not_dramatic":true,"cream_or_stone_surface_required":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "brand name, labels between socks, cartoon, illustration, 3d render, badge, CTA button, colourful socks, athletic socks, white background, person wearing, face",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c33",
        "concept": "33 — Bathroom Floor Morning Discovery",
        "swipe_ref": "ID 052 — SCR-20260313-bohi.jpeg (shock-reframe)",
        "prompt": '{"style":"Candid documentary close-up — bathroom floor, morning. The moment of noticing something that has been quietly happening.","lighting":"Warm bathroom light — overhead practical lighting, slightly warm and unglamorous. Tile floor visible.","scene":"Tight shot from above — a foot on bathroom tile floor, cotton sock on the foot, shot from ankle level or slightly above. The heel of the sock is worn through — a clear hole or heavily thinned patch. The foot is at rest on the tile. No person visible above the ankle. Bold headline overlaid at top.","primary_object":{"description":"The sock on the bathroom floor — the problem is visible without explanation","sock_heel_detail":"Dark cotton sock, heel area with visible hole or heavily worn patch. The damage is in sharp focus. The tile floor is in soft focus behind.","foot_detail":"At rest on tile. Only foot and ankle visible. Not athletic — the context is a practical morning getting-ready moment."},"supporting_objects":[],"energy":"Stood on the cold tile and felt the gap. That was three months ago. Nothing changed.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame","weight":"heavy/black"},"constraints":{"heel_hole_or_damage_must_be_clear_focal_point_in_sharp_focus":true,"NOT_above_ankle_in_frame":true,"bathroom_tile_context_required":true,"NOT_athletic_or_gym_context":true,"NOT_brand_name_on_sock":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "above ankle, face, person above ankle, gym, athletic, studio, white background, brand name, clean undamaged sock, colourful tile, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c34",
        "concept": "34 — Single Line Proof Statement Dark",
        "swipe_ref": "ID 045 — SCR-20260313-bnre.jpeg (problem-agitate-lifestyle)",
        "prompt": '{"style":"Pure typographic dark card — stark and confrontational. One statement. Nothing else. The silence around the text is part of the argument.","lighting":"Not applicable — flat dark background.","scene":"Full bleed near-black background. The headline text centred in the frame, white heavy sans-serif. Very large — the text fills the frame with generous margin. No image, no product, no decoration. The weight of the type is the entire ad.","primary_object":{"description":"The headline text alone","headline_detail":"White heavy black-weight sans-serif. Very large leading. Text: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Centred. The size makes it feel like a statement being made at volume, not printed."},"supporting_objects":[],"energy":"No hedging. No qualification. Just the claim.","constraints":{"headline_content_exact":"5 Reasons 100% Cotton Socks Are Designed to Fail You","NOT_any_other_text_present":true,"dark_background_required":true,"text_must_be_centred_and_dominant":true,"NOT_product_image_or_decorative_elements":true}}',
        "negative_prompt": "colourful background, white background, product image, decorative elements, sub-text, badge, brand name, person, lifestyle, cartoon, illustration, 3d render, CTA button, gradient",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c35",
        "concept": "35 — Desk Beside the Sock — Evidence Flat Lay",
        "swipe_ref": "ID 103 — SCR-20260313-bubh.png (side-by-side-comparison)",
        "prompt": '{"style":"Overhead flat lay — the desk as a thinking surface. Evidence arranged deliberately.","lighting":"Warm desk lamp light from one side — practical indoor. Not corrected.","scene":"Overhead shot of a desk surface. Arranged on the desk: one dark worn cotton sock with visible heel damage placed centrally, a pen resting next to it, and a small piece of paper or sticky note with the headline written by hand. The objects look like they were placed there by someone making a point to themselves. Nothing styled — functional and real.","primary_object":{"description":"The worn sock and handwritten note on desk surface","sock_detail":"Dark sock with clear heel damage. Placed on desk as an exhibit.","note_detail":"Small piece of paper or sticky note beside the sock. Handwritten: 5 Reasons 100% Cotton Socks Are Designed to Fail You. The handwriting is the only legible text.","pen_detail":"A pen resting nearby — someone just wrote this."},"supporting_objects":[],"energy":"He placed it there deliberately. The sock is exhibit A.","constraints":{"headline_appears_only_on_handwritten_note_no_separate_overlay":true,"handwritten_note_text_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","sock_damage_must_be_visible":true,"NOT_brand_name_on_sock_or_note":true,"overhead_shot_required":true,"NOT_other_legible_text_in_image":true}}',
        "negative_prompt": "brand name, typed text on screen, digital display, other legible text, clean undamaged sock, studio shot, white background, person, face, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c36",
        "concept": "36 — Man Seated — Trouser Hem Side Profile",
        "swipe_ref": "ID 068 — SCR-20260313-bqut.jpeg (myth-buster-proof)",
        "prompt": '{"style":"Editorial documentary side-profile — seated man, the detail is at the ankle. Candid, not posed.","lighting":"Natural office or home light from a window — soft directional light, slightly warm. Practical environment.","scene":"Side-profile tight crop of a man seated — visible from mid-calf to floor, or thigh to floor. Dark smart trousers, leather shoes. The sock is visible at the trouser hem and clearly shows a slack or dropped cuff — the elastic has given up. The environment: chair leg visible, office floor or wooden floor. The man is not the subject — the ankle detail is. Bold headline at top.","primary_object":{"description":"The seated ankle detail — the problem is visible at rest","sock_at_hem_detail":"Dark or grey cotton sock at trouser hem. Cuff slack or dropped — not sitting flush. The elastic memory failure is visible even when he is sitting still.","environment_detail":"Office chair leg, floor surface. Practical and real.","crop":"Mid-calf or thigh to floor, side profile. Face not required."},"supporting_objects":[],"energy":"He is sitting at his desk. He has not looked down yet. We have.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame","weight":"heavy/black"},"constraints":{"crop_is_mid_calf_to_floor_or_thigh_to_floor":true,"sock_cuff_slack_or_dropped_must_be_visible":true,"NOT_looking_at_camera":true,"NOT_athletic_shoes_leather_or_smart_only":true,"NOT_brand_name_on_sock_or_shoes":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "full portrait with face prominent, smiling at camera, gym, athletic shoes, sneakers, sportswear, studio, clean perfect sock, brand name, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c37",
        "concept": "37 — DM Screenshot Format",
        "swipe_ref": "ID 005 — SCR-20260313-biiu.png (social post register)",
        "prompt": '{"style":"Direct message screenshot — one person sent this to another. Platform mimicry: iMessage or WhatsApp style. The intimacy of a shared recommendation.","lighting":"Not applicable — screen simulation.","scene":"A phone screen showing a DM conversation. Two bubbles visible. First bubble from the other person: just a link — a URL to a consumer guide article. The link preview card shows: title in bold type (the headline), a small worn sock thumbnail image. Second bubble below from the recipient: a thumbs up or simple acknowledgement reaction. That is the full composition.","primary_object":{"description":"The DM thread with the shared link","link_preview_card_detail":"Article title bold: 5 Reasons 100% Cotton Socks Are Designed to Fail You. Small worn sock image thumbnail on the right of the card. URL below in grey — generic consumer guide URL, not a brand domain.","bubble_detail":"First bubble: link card only — no other text. Second bubble: single emoji reaction or very short reply — nothing that competes with the headline.","interface_detail":"Standard iMessage or WhatsApp interface. Grey and white bubbles. Clean."},"supporting_objects":[],"energy":"A friend sent this without context. That is enough.","constraints":{"headline_appears_only_in_link_preview_card":"5 Reasons 100% Cotton Socks Are Designed to Fail You","link_preview_must_show_worn_sock_thumbnail":true,"NOT_brand_URL_in_link_preview":true,"interface_must_look_authentic":true,"NOT_other_legible_text_besides_headline_in_card_and_short_reaction":true}}',
        "negative_prompt": "brand domain URL, long text message, brand logo, cartoon, illustration, 3d render, badge, CTA button, desktop interface, email format, other article headlines",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c38",
        "concept": "38 — Waste Bin Full of Discarded Socks",
        "swipe_ref": "ID 052 — SCR-20260313-bohi.jpeg (shock-reframe)",
        "prompt": '{"style":"Documentary close-up — the evidence of the pattern. Not one failed sock — the accumulated cost of the category.","lighting":"Warm domestic ambient light — bedroom or bathroom bin. Slightly warm and unglamorous.","scene":"A small household bin or waste basket, photographed from slightly above. Inside: 3-4 discarded cotton socks — some with visible heel holes, one with elastic completely gone, one simply pilled and worn out. Not a dramatic pile — a practical bin with the ordinary accumulated waste of the cotton sock habit. Bold headline overlaid at top.","primary_object":{"description":"The bin contents — accumulated evidence","bin_contents_detail":"3-4 discarded dark cotton socks in various failure states: heel hole, collapsed elastic, surface pilling. Real domestic bin — not styled.","bin_detail":"Plain household bin, small — bathroom or bedroom type. Nothing glamorous about the container."},"supporting_objects":[],"energy":"He throws them away and buys another pack. Every three months. Without asking why.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame","weight":"heavy/black"},"constraints":{"bin_must_contain_multiple_failed_socks_in_different_states":true,"NOT_brand_name_on_any_sock":true,"NOT_styled_or_aesthetic_bin":true,"practical_domestic_context_required":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "one sock only, clean undamaged socks, brand name, styled aesthetic bin, studio, white background, person, face, gym, athletic socks, colourful socks, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c39",
        "concept": "39 — Man At Door — Leaving The House",
        "swipe_ref": "ID 116 — SCR-20260313-bvmm.jpeg (editorial magazine register)",
        "prompt": '{"style":"Documentary lifestyle lower-body crop — the moment before the commute. The detail is in the hem.","lighting":"Morning indoor light near an entrance — warm, practical, slightly backlit from a window or door.","scene":"A man near a front door or entrance, in the act of leaving — he is at a slight angle, mid-stride or reaching for a coat. The shot is from thigh to floor — dark smart trousers, leather shoes. The sock at the trouser hem is visible, cuff slightly displaced. The entrance context is clear: coat, door, morning light. The person is anonymous — only lower body visible. Bold headline at top.","primary_object":{"description":"The leaving-the-house lower body — the sock detail is part of the morning routine","entrance_context_detail":"Door edge, coat, or bag visible in frame. Morning departure context.","sock_at_hem_detail":"Cuff slightly displaced or slack — the small habitual problem he takes with him every day."},"supporting_objects":[],"energy":"He leaves with it every morning. He will notice it by 10am.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top","weight":"heavy/black"},"constraints":{"crop_must_be_thigh_to_floor_maximum":true,"entrance_or_departure_context_required":true,"sock_displacement_visible_at_hem":true,"NOT_athletic_shoes_leather_or_smart_only":true,"NOT_looking_at_camera_not_posed":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "full portrait face visible, gym, athletic shoes, sneakers, sportswear, studio, clean perfect sock, brand name, cartoon, illustration, 3d render, badge, CTA button, smiling at camera",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c40",
        "concept": "40 — Bold Claim on Warm Cream Background",
        "swipe_ref": "ID 076 — SCR-20260313-bsht.jpeg (pattern-interrupt-paradox)",
        "prompt": '{"style":"Pattern interrupt minimal — warm background, massive type, tiny product. The unexpected calm of the composition under the alarming headline.","lighting":"Not applicable — flat warm cream or sage green background.","scene":"Warm cream or muted sage green background — unexpected for a sock ad. The headline text dominates the upper three-quarters of the frame in very large bold type. At the very bottom, small and understated: a single neat dark rolled sock. Nothing else.","primary_object":{"description":"The headline dominates — the sock is deliberately small","headline_detail":"Heavy bold black or very dark type. Very large — takes up most of the vertical frame. Text: 5 Reasons 100% Cotton Socks Are Designed to Fail You.","product_detail":"One small neat dark rolled sock at bottom centre — approximately 10% of frame height. No brand name."},"supporting_objects":[],"energy":"The calm object below the alarming claim.","constraints":{"headline_must_dominate_composition":true,"sock_must_be_small_and_subordinate":true,"background_must_be_warm_cream_or_muted_sage_NOT_white":true,"NOT_brand_name_on_sock":true,"headline_is_the_only_text_in_image":true,"headline_content_exact":"5 Reasons 100% Cotton Socks Are Designed to Fail You"}}',
        "negative_prompt": "white background, dark background, bright saturated colour, brand name, lifestyle, person, face, sub-copy text, busy composition, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c41",
        "concept": "41 — Man At Desk — Mid-Morning Reach Down",
        "swipe_ref": "ID 045 — SCR-20260313-bnre.jpeg (problem-agitate-lifestyle)",
        "prompt": '{"style":"Candid office documentary — caught in the act. Not a posed moment.","lighting":"Office ambient light — overhead fluorescent or warm desk lamp. Practical indoor environment.","scene":"A man at an office desk, seen from the side or slightly behind — he is mid-reach, bending sideways in his chair to pull up the sock at his ankle under the desk. The posture is awkward and habitual — not a dramatic gesture, just the ordinary mid-morning correction. His face is not important — the gesture is. Bold headline at top.","primary_object":{"description":"The sideways reach in the chair — the habitual mid-morning correction","gesture_detail":"Seated man bending sideways, arm extended down toward ankle. The gesture of someone who has done this a hundred times. Not performing it — doing it.","desk_context_detail":"Desk surface visible — keyboard, papers. Office chair. Practical work environment.","crop":"The man is visible to the mid-torso at most — the focus is the bent posture and the ankle."},"supporting_objects":[],"energy":"Third time this morning. He is barely aware he is doing it.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of image","weight":"heavy/black"},"constraints":{"man_must_be_mid_reach_toward_ankle_while_seated":true,"NOT_posed_or_looking_at_camera":true,"office_context_required":true,"NOT_gym_or_athletic_context":true,"habitual_gesture_not_dramatic_expression":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "looking at camera, smiling, dramatic expression, gym, athletic, studio lighting, fashion model, full portrait, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c42",
        "concept": "42 — Overhead Socks On Wooden Floor",
        "swipe_ref": "ID 022 — SCR-20260313-bksr.jpeg (documentary prop register)",
        "prompt": '{"style":"Overhead documentary flat lay — stripped back. No surface preparation, no styling. The floor is the stage.","lighting":"Natural window light from the side — warm hardwood floor, slight shadow from the weave texture of the sock.","scene":"Overhead shot of a hardwood wooden floor. A single dark cotton sock laid flat — slightly crumpled as if just taken off, not laid out neatly. The heel area shows clear wear — thinning or early hole. Nothing else on the floor. The simplicity of the composition is the point. Bold headline overlaid at top or bottom.","primary_object":{"description":"The sock on the floor — not staged, just placed","sock_detail":"Dark navy or charcoal cotton sock. Slightly crumpled — as if just removed. Heel zone visibly worn. No brand markings.","floor_detail":"Warm hardwood floor. Natural grain. The sock sits on it as an exhibit, not a product shot."},"supporting_objects":[],"energy":"Taken off at the end of the day. The heel is already gone.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at bottom of image, full width, against the dark sock or hardwood","weight":"heavy/black"},"constraints":{"sock_must_look_just_removed_not_neatly_arranged":true,"heel_damage_visible":true,"NOT_brand_name_on_sock":true,"hardwood_floor_required":true,"overhead_shot":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "neat styled flat lay, white background, brand name, clean undamaged sock, studio, colourful surface, person, face, athletic, gym, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c43",
        "concept": "43 — Glasses Man — Side Profile Reading",
        "swipe_ref": "ID 071 — SCR-20260313-brbu.jpeg (testimonial-discovery register)",
        "prompt": '{"style":"Side profile UGC close-crop — the face of someone processing new information. Phone camera quality, natural, not posed.","lighting":"Natural window light from the front — slightly warm, directional. Side profile so the light catches one cheekbone and the frame of the glasses.","scene":"Close crop side profile of a man, 50s, wearing glasses — he is looking down and to the side, slightly forward, reading something. The glasses frames are prominent in profile. Expression: the look of someone who is mildly annoyed they did not know this already. Bold headline overlaid across the lower half of the image.","primary_object":{"description":"The side-profile close crop — the expression of discovery","glasses_detail":"Classic or round frames in side profile. Worn on face, not held.","expression_detail":"Looking down at something being read. Brow slightly furrowed. Not dramatic — the low-key mildly annoyed expression of a practical man encountering a reframe.","crop":"Head and upper chest only, side profile."},"supporting_objects":[],"energy":"He read it. He went quiet for a moment. Then kept reading.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type lower half of image directly on photo","weight":"heavy/black"},"constraints":{"side_profile_required_not_front_facing":true,"glasses_worn_on_face_not_held":true,"NOT_smiling_or_looking_at_camera":true,"expression_must_be_quiet_and_processing_not_dramatic":true,"headline_is_the_only_text_in_image":true,"NOT_studio_quality_lighting":true}}',
        "negative_prompt": "front-facing portrait, smiling, glasses held not worn, studio lighting, stock photo expression, gym, athletic, fashion, text in card box, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c44",
        "concept": "44 — Cold Morning Foot Close-Up",
        "swipe_ref": "ID 011 — SCR-20260313-bjqv.jpeg (detail register)",
        "prompt": '{"style":"Documentary close-up — the morning foot, the cold tile, the worn sock. Intimate and specific.","lighting":"Cool morning light from a window — slightly blue-grey. Tile or stone floor. The light is early and practical.","scene":"Close shot from above of a foot in a cotton sock standing on a cold-looking tile or stone floor. The sock shows its age — slight pilling on the surface, the cuff slightly loose. Not dramatically damaged — just clearly not in its first year. The heel zone is visible and slightly worn. The cold floor texture is visible at the edges. Bold headline at top.","primary_object":{"description":"The foot in its worn sock on the cold morning floor","sock_detail":"Grey or dark cotton sock. Cuff slightly loose. Surface slightly pilled. Heel zone showing wear. Not new.","floor_detail":"Cold tile or stone. Grey or off-white. The practical morning surface.","crop":"Ankle and foot only — no person above the ankle."},"supporting_objects":[],"energy":"6:45am. Cold floor. The sock is the wrong tool for this.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame","weight":"heavy/black"},"constraints":{"crop_is_ankle_and_foot_only_nothing_above":true,"cold_tile_or_stone_floor_required":true,"sock_must_show_age_not_brand_new":true,"NOT_athletic_context":true,"NOT_brand_name_on_sock":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "above ankle, face, person above ankle, gym, athletic, studio, brand new clean sock, brand name, colourful tile, warm cosy aesthetic, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c45",
        "concept": "45 — Receipts and Sock Pile",
        "swipe_ref": "ID 007 — SCR-20260313-bilv.jpeg (social screenshot register)",
        "prompt": '{"style":"Overhead flat lay evidence — the financial reality of the cotton sock habit assembled on a surface.","lighting":"Warm overhead lamp or window light — kitchen counter or desk surface. Practical.","scene":"Overhead shot of a flat surface. A small pile of 3 dark cotton socks in various states of wear — one with a heel hole, one pilled. Beside the pile: 2 or 3 supermarket or convenience store receipts, slightly crumpled — one circled item with a pen mark (presumably the sock purchase). The composition looks like someone assembling the evidence of a habit. The handwritten headline on a sticky note is the only legible text.","primary_object":{"description":"The sock pile and receipts — the cost of the habit","sock_pile_detail":"3 dark cotton socks in varying wear states. The damage is visible.","receipts_detail":"Supermarket or general store receipts, slightly crumpled. One has a circled line item — the repeated purchase. Receipts are not fully legible — just the material texture of documented spending.","sticky_note_detail":"Small sticky note beside the pile. Handwritten: 5 Reasons 100% Cotton Socks Are Designed to Fail You. The headline is the only legible text."},"supporting_objects":[],"energy":"The same purchase. Every three months. For twenty years.","constraints":{"headline_appears_only_on_sticky_note_no_separate_overlay":true,"sticky_note_text_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","receipt_line_item_circled_in_pen_required":true,"NOT_full_receipt_text_legible":true,"sock_damage_visible_in_pile":true,"NOT_brand_name_on_socks_or_receipts":true}}',
        "negative_prompt": "brand name, fully legible receipt, digital display, studio, white background, person, face, athletic, colourful, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c46",
        "concept": "46 — Walking Shot From Behind",
        "swipe_ref": "ID 068 — SCR-20260313-bqut.jpeg (full-bleed person register)",
        "prompt": '{"style":"Street candid from behind — the person walking away. The sock is the last thing visible before they disappear.","lighting":"Natural outdoor urban light — overcast or afternoon. City pavement or path. Slightly cool.","scene":"A man walking away from the camera on a city pavement — seen from behind, from about knee-height up or full body from behind. Dark smart trousers, leather shoes. At the trouser hem: the sock is visible and the cuff has slipped — the gap or dropped cuff is clear on one ankle. He is mid-stride, slightly blurred, walking. The headline overlaid at top.","primary_object":{"description":"The man from behind — the sock detail at the hem as he walks","walking_posture":"Mid-stride, slight movement blur acceptable. Not aware of camera. Moving purposefully.","sock_at_hem_detail":"Dark sock, cuff slipped on one ankle — the asymmetry of one ankle tight and one loose is visible in walking.","environment_detail":"Urban pavement, slightly blurred background buildings or parked cars."},"supporting_objects":[],"energy":"He walks out every day with the same problem. He has never named it.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame, full width","weight":"heavy/black"},"constraints":{"from_behind_shot_required_face_not_visible":true,"sock_cuff_slippage_visible_on_one_ankle_while_walking":true,"urban_outdoor_environment_required":true,"NOT_athletic_shoes_leather_or_smart_only":true,"NOT_posed_or_studio":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "face visible from front, smiling, posed, studio, gym, athletic shoes, sneakers, sportswear, brand name, clean perfect sock, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c47",
        "concept": "47 — End of Day Shoe Removal",
        "swipe_ref": "ID 083 — SCR-20260313-btab.jpeg (detail-shot register)",
        "prompt": '{"style":"Intimate documentary — the private end-of-day moment. The evidence is the sock that comes off with the shoe.","lighting":"Warm evening indoor light — entrance hallway or living room floor. Warm and practical.","scene":"A man seated, removing one leather shoe — seen from knee to floor. The shoe is half-off. The sock visible at the ankle is showing its age: slightly slack at the cuff, possibly pilling at the ankle. The floor has one shoe already removed beside the foot. The other shoe is being taken off. Bold headline at top.","primary_object":{"description":"The end-of-day shoe removal — the sock comes into view","shoe_removal_detail":"One leather shoe half removed from foot, held at the heel. The sock is exposed at the ankle in this moment.","sock_detail":"Dark cotton sock at ankle. Cuff slightly slack. Surface showing some wear. Not dramatic — just not holding up.","floor_detail":"One shoe already placed on floor beside the foot. Practical hallway or entry context."},"supporting_objects":[],"energy":"The small private admission at the end of the day.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top","weight":"heavy/black"},"constraints":{"shoe_removal_in_progress_required":true,"sock_must_be_visible_during_removal":true,"NOT_athletic_shoes_leather_required":true,"NOT_above_knee_in_frame":true,"NOT_brand_name_on_sock_or_shoe":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "athletic shoes, sneakers, above knee, face, gym, studio, brand name, clean new sock, colourful, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c48",
        "concept": "48 — Proof Board Photo Wall",
        "swipe_ref": "ID 299 — 045465c8-0a0f-48b8-953c-248125b625ab.jpeg (protest-sign register)",
        "prompt": '{"style":"Evidence board documentary — the photo pinned to a board. Investigative register.","lighting":"Warm practical light — home office or study. Slightly low-key.","scene":"A pinboard or cork board, photographed from slightly below eye level. Pinned to the board: the headline on a large piece of white paper — printed or written in bold type. Below it: two small printed photos of worn sock damage — heel holes, pilling. A few push pins. The board is practical — slightly crowded with other indistinct pinned items around the edges that are blurred or unreadable. The headline is the focal point.","primary_object":{"description":"The pinboard with the headline and sock damage photos","headline_pinned_detail":"Large white paper or printout pinned to board. Bold type: 5 Reasons 100% Cotton Socks Are Designed to Fail You. The headline is the centrepiece.","sock_damage_photos_detail":"Two small printed photos below the headline, pinned. One shows a heel hole. One shows pilling on a surface. Black and white or colour — practical printouts, not styled.","surrounding_pins_detail":"Other items pinned around the edges — blurred and illegible. Background texture only."},"supporting_objects":[],"energy":"Someone built the case before writing the article.","constraints":{"headline_on_pinned_paper_must_be_legible":"5 Reasons 100% Cotton Socks Are Designed to Fail You","sock_damage_photos_must_be_visible_below_headline":true,"NOT_brand_name_on_any_element":true,"surrounding_pinned_items_must_be_blurred_or_illegible":true,"investigative_pinboard_register_required":true,"headline_is_the_only_legible_text_in_image":true}}',
        "negative_prompt": "brand name, other legible text on board, clean perfect socks in photos, digital display, cartoon, illustration, 3d render, badge, CTA button, styled interior",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c49",
        "concept": "49 — Quiet Man Looking Down",
        "swipe_ref": "ID 005 — SCR-20260313-biiu.png (founder-letter register)",
        "prompt": '{"style":"UGC intimate portrait — the look of someone absorbing something that shifts a long-held assumption. Close, real, imperfect framing.","lighting":"Soft indoor window light — warm, slightly diffused. Not corrected. Real room behind him.","scene":"Close crop of a man, 40s-50s, looking straight down — not at camera, not to the side, just down. The expression is neutral and slightly inward — processing, not reacting. Head and upper chest only. The background is a plain wall or window light behind. Bold headline overlaid at the bottom of the image directly on the photo.","primary_object":{"description":"The man looking down — the posture of someone who just read something","posture_detail":"Head tilted slightly forward and down. Not dramatic. The quiet absorption of new information.","expression_detail":"Neutral, slightly inward. Not worried, not angry — just thinking. The face of a practical man encountering a reframe.","crop":"Head and upper chest. Slightly tight — UGC close-crop energy."},"supporting_objects":[],"energy":"He read the headline. He has not looked up yet.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at bottom of image directly on photo","weight":"heavy/black"},"constraints":{"NOT_looking_at_camera_looking_straight_down":true,"NOT_smiling_or_reacting_dramatically":true,"expression_must_be_quiet_and_inward":true,"NOT_studio_quality_lighting":true,"UGC_close_crop_head_and_chest_only":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "looking at camera, smiling, dramatic expression, studio lighting, stock photo pose, gym, athletic, glasses (not required), fashion, text in card box, cartoon, illustration, 3d render, badge",
        "aspect_ratio": "4:5",
    },
    {
        "id": "c50",
        "concept": "50 — Long Shadow Legs Pavement",
        "swipe_ref": "ID 116 — SCR-20260313-bvmm.jpeg (editorial magazine register)",
        "prompt": '{"style":"High contrast editorial street photography — the shadow does the storytelling. Graphic and minimal.","lighting":"Strong directional sunlight — morning or late afternoon, low angle. The shadow is long and sharp on the pavement. High contrast.","scene":"Pavement shot from above — a man is standing still or mid-stride on a city pavement, shot from directly above or at a very high angle. What we see: the top of his head, his shoulders, and the long dramatic shadow stretching ahead of him on the stone pavement. His feet are at the bottom of frame — dark leather shoes, and at the trouser hem, one sock cuff just slightly dropped. The shadow is the graphic element. Bold headline at top.","primary_object":{"description":"The overhead or high-angle shot — the long shadow on the pavement","shadow_detail":"Long sharp shadow stretching ahead of the man on light stone pavement. High contrast — light and dark.","figure_detail":"Seen from above — top of head and shoulders. Feet at bottom of frame.","sock_at_hem_detail":"One ankle shows sock cuff slightly dropped — visible from the high angle at the trouser hem."},"supporting_objects":[],"energy":"He stands on the pavement. His shadow goes ahead of him. The sock goes down behind.","headline_overlay":{"text":"5 Reasons 100% Cotton Socks Are Designed to Fail You","placement":"bold white heavy type at top of frame against the light pavement or sky","weight":"heavy/black"},"constraints":{"overhead_or_very_high_angle_shot_required":true,"long_dramatic_shadow_on_pavement_required":true,"sock_cuff_displacement_visible_at_hem_from_above":true,"NOT_looking_at_camera":true,"pavement_must_be_light_coloured_for_shadow_contrast":true,"headline_is_the_only_text_in_image":true}}',
        "negative_prompt": "flat even lighting, no shadow, facing camera, gym, athletic shoes, studio, brand name, clean perfect sock, colourful pavement, cartoon, illustration, 3d render, badge, CTA button",
        "aspect_ratio": "4:5",
    },
]


def save_image_from_url(image_url: str, prompt_id: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prompt_id}_{timestamp}.png"
    filepath = output_dir / filename

    response = urllib.request.urlopen(image_url)
    image_bytes = response.read()
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    latest_path = output_dir / f"{prompt_id}.png"
    with open(latest_path, "wb") as f:
        f.write(image_bytes)

    return filepath


def generate_image(prompt_data: dict):
    try:
        result = fal_client.subscribe(
            "fal-ai/nano-banana-2",
            arguments={
                "prompt": prompt_data["prompt"],
                "negative_prompt": prompt_data["negative_prompt"],
                "aspect_ratio": prompt_data["aspect_ratio"],
                "resolution": "2K",
                "num_images": 1,
                "output_format": "png",
            },
        )

        if result and "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        return None

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate Mat & Vic's ad concept images via NB2")
    parser.add_argument("--ids", type=str, help="Comma-separated IDs (c01,c02) or 'all'")
    parser.add_argument("--list", action="store_true", help="List all prompts")
    args = parser.parse_args()

    if args.list:
        print(f"\n=== Mat & Vic's Ad Concept Image Prompts ({len(PROMPTS)} total) ===\n")
        for p in PROMPTS:
            print(f"  {p['id']}: {p['concept']}")
            print(f"       Swipe: {p['swipe_ref']}")
        return

    if not args.ids:
        print("Usage:")
        print("  python3 generate_ad_images.py --ids all")
        print("  python3 generate_ad_images.py --ids c01,c03")
        print("  python3 generate_ad_images.py --list")
        return

    if fal_client is None:
        print("ERROR: fal-client not installed. Run: pip install fal-client")
        sys.exit(1)

    FAL_KEY = os.environ.get("FAL_KEY", "")
    if not FAL_KEY:
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("FAL_KEY="):
                    FAL_KEY = line.split("=", 1)[1].strip()
                    break
    if not FAL_KEY:
        print("ERROR: FAL_KEY not set. Run: export FAL_KEY=your_key_here")
        print("Get your key at: https://fal.ai/dashboard")
        sys.exit(1)
    os.environ["FAL_KEY"] = FAL_KEY

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.ids.lower() == "all":
        to_generate = PROMPTS
    else:
        ids = [x.strip().lower() for x in args.ids.split(",")]
        to_generate = [p for p in PROMPTS if p["id"] in ids]
        if not to_generate:
            print(f"No prompts found for: {args.ids}")
            print("Use --list to see available IDs")
            return

    print(f"\n{'='*60}")
    print(f"MAT & VIC'S AD CONCEPT IMAGE GENERATOR — 50 CONCEPTS (fal-ai/NB2)")
    print(f"{'='*60}")
    print(f"Images to generate: {len(to_generate)}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    successful = 0
    failed = 0

    for i, prompt_data in enumerate(to_generate, 1):
        print(f"[{i}/{len(to_generate)}] {prompt_data['id']}: {prompt_data['concept']}")
        print(f"  Reason {prompt_data['reason']} | {prompt_data['swipe_ref']}")

        image_url = generate_image(prompt_data)

        if image_url:
            filepath = save_image_from_url(image_url, prompt_data["id"], OUTPUT_DIR)
            print(f"  Saved: {filepath}")
            successful += 1
        else:
            print(f"  FAILED")
            failed += 1

        if i < len(to_generate):
            print(f"  Waiting {DELAY_BETWEEN}s...")
            time.sleep(DELAY_BETWEEN)

    print(f"\n{'='*60}")
    print(f"COMPLETE: {successful}/{len(to_generate)} images")
    if failed > 0:
        print(f"Failed: {failed}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
