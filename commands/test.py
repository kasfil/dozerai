import os
from pathlib import Path

from telegram import Update, error as tele_error
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from helper.msg_sender import send_messages
from config import GROUP_PATH, MAX_MSG_CHARS
from helper.mdconverter import to_telemd

base_reply = """# Sample Document

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus interdum nisl at sem pretium malesuada. **Curabitur vitae nibh at turpis** elementum sollicitudin. Maecenas quis ligula venenatis, varius justo ut, convallis erat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer et feugiat leo.

## Section 1: Introduction

Lorem ipsum dolor sit amet, *consectetur adipiscing* elit. Suspendisse efficitur nunc non ex facilisis blandit. Integer feugiat ligula eget nisl consectetur accumsan. Pellentesque in **ligula at libero** suscipit malesuada et ut lorem. Vivamus fermentum urna nec *porttitor* placerat. Cras fermentum feugiat dolor, sed interdum libero tincidunt in. Morbi id augue ut erat luctus blandit nec a nisl.

- Vivamus malesuada lacinia arcu
- Maecenas tincidunt felis
- Proin nec feugiat risus

1. **Mauris** viverra tortor quis nibh dignissim
2. In eget *lectus ac*
3. Curabitur ornare, arcu ut feugiat

Nam aliquet tellus in dolor tempor, et **vehicula mauris** viverra. Duis facilisis augue eget magna feugiat, nec suscipit nibh ultricies. *Donec id risus* nec velit sollicitudin tincidunt id ut risus.

## Section 2: Overview of Concepts

Vivamus aliquam condimentum nulla, sed bibendum ligula efficitur id. **Pellentesque habitant morbi** tristique senectus et netus et malesuada fames ac turpis egestas. Duis posuere ac nunc sed scelerisque. Nulla convallis lectus id fermentum tempor. Pellentesque sollicitudin sem et est tempor tristique. Fusce tincidunt turpis non lectus malesuada dignissim.

1. **Lorem ipsum** dolor sit amet, consectetur adipiscing elit. Aliquam pharetra est felis, sed vestibulum lectus egestas ac.
   - Nulla condimentum nisl ac sapien venenatis
   - Cras venenatis quam in felis fringilla laoreet
2. Fusce ut velit suscipit, facilisis velit id, pulvinar purus. Aenean at arcu non metus hendrerit laoreet.

### Subheading 1: Key Elements

*Ut convallis lacus* non urna ultricies faucibus. Phasellus feugiat blandit orci et **porttitor**. Nulla facilisi. In aliquam tortor orci, eu volutpat mi malesuada eget. Morbi volutpat neque nisi, nec scelerisque nisl fringilla et. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec cursus urna ut metus facilisis ornare.

- *Vestibulum* ante ipsum primis in faucibus
- Fusce ultrices enim et nunc
- Nam malesuada urna at lectus tempor

1. Suspendisse **ullamcorper**
2. Donec ultricies erat
3. *Cras* sagittis placerat

## Section 3: Practical Applications

Etiam elementum lectus vel diam hendrerit, id laoreet enim fermentum. Integer sagittis consequat diam, a faucibus erat convallis id. Maecenas in neque ac sapien pulvinar tincidunt. Suspendisse potenti. Pellentesque *id euismod dui*, eget scelerisque felis. Aliquam erat volutpat.

1. **Vivamus egestas** felis non massa fermentum laoreet
2. Aenean sit amet nibh lorem, a *ultrices turpis*
3. Ut efficitur turpis id justo ultricies

*Quisque at urna*, pharetra magna sit amet, condimentum nunc. Fusce **vel nibh** eu massa fringilla auctor et id ligula. In volutpat magna ut fermentum dictum. Nam quis nibh orci.

### Subheading 2: List Examples

- Cras nec neque in arcu
- Etiam sed urna nec sapien pulvinar facilisis
- Aliquam id augue et felis dictum egestas

In luctus risus a metus tristique pharetra. **Phasellus** condimentum sem et justo sagittis, sed dapibus lacus venenatis. Integer luctus facilisis ligula. Maecenas fermentum libero eu lorem convallis, vel congue justo varius.

1. Proin consequat velit at erat consequat
2. *Morbi sed tortor nec* sapien pulvinar vestibulum
3. Vivamus ac elit fringilla nisl facilisis

Fusce sagittis, libero nec pharetra finibus, lorem dui *laoreet dolor*, nec bibendum mi dui sit amet risus. Cras tincidunt magna sit amet purus fermentum, nec lacinia ante fermentum. Phasellus id sapien id quam aliquet dictum.

## Section 4: Expanding on Practical Applications

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Praesent nec maximus felis, sed *elementum magna*. Morbi sit amet tortor fringilla, tincidunt nisi id, vehicula lacus. Nulla eget scelerisque arcu. Mauris lacinia sit amet nibh et sollicitudin. Donec eget velit at risus tincidunt hendrerit. Cras viverra lectus vitae tempor cursus. Phasellus condimentum erat euismod venenatis vehicula.

### Subheading 3: Detailed Lists

1. **Integer pretium** odio eget orci fermentum, at sollicitudin magna pharetra.
2. Sed sit amet risus velit, non venenatis lorem.
3. Phasellus consequat, tortor sit amet facilisis sagittis, justo magna interdum lorem, non tempor sapien nisl ac ligula.

#### Unordered List Examples

- Vivamus id ligula eget arcu consequat hendrerit
- Phasellus vel risus laoreet, *faucibus lacus et*, iaculis odio
- Sed euismod felis vel magna sagittis

## Section 5: Conclusion

In finibus, nisl a laoreet cursus, sapien orci vehicula nisi, vel tempus augue nisl et ante. Curabitur auctor ex sed tortor fringilla, vitae dictum magna convallis. **Sed accumsan**, nisi id vestibulum eleifend, magna elit hendrerit eros, a ullamcorper leo nisl vel sapien.

*Thank you for reading this extended document!*
"""


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /ask is issued."""
    if not update.effective_message or not update.message or not update.message.text:
        return

    converted = to_telemd(base_reply)
    await send_messages(update, [converted])

    # # Check if response image is longer than 8000 characters then cut each 8000 characters
    # # and send it as separate message
    # if len(converted) > MAX_MSG_CHARS:
    #     for i in range(0, len(converted), MAX_MSG_CHARS):
    #         await update.message.reply_markdown_v2(
    #             converted[i : i + MAX_MSG_CHARS],
    #         )

    # else:
