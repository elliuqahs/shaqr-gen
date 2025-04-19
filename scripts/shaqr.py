from lib.qrcodegen import QrCode, QrSegment
from PIL import Image
import io
import base64

class ShaQR:
    def __to_base4_bits(self, text):
        binary = ''.join(f'{ord(c):08b}' for c in text)
        return [binary[i:i+2] for i in range(0, len(binary), 2)]

    def __encode_zwc(self, text, hidden):
        zwc_map = {'00': '\u200b', '01': '\u200c', '10': '\u200d', '11': '\u2060'}
        bits = self.__to_base4_bits(hidden)
        zwc_encoded = ''.join(zwc_map[b] for b in bits)
        return text + zwc_encoded


    def __find_best_mask(self, text):
        best_score = float("inf")
        best_mask = None

        for mask in range(8):
            qr = QrCode.encode_segments([QrSegment.make_bytes(text.encode("utf-8"))],QrCode.Ecc.LOW, mask=mask)
            score = qr._get_penalty_score()
            print(f"Mask {mask} has penalty score: {score}")

            if score < best_score:
                best_score = score
                best_mask = mask
        
        return best_mask, best_score

    def create_sha_qr(self,visible_text):
        visible = visible_text
        hidden = "shaqQR"
        text = self.__encode_zwc(visible, hidden)
        best_mask, best_score = self.__find_best_mask(visible)

        print(f"Recommended mask: {best_mask} with score {best_score}")

        qr = QrCode.encode_segments([QrSegment.make_bytes(text.encode("utf-8"))],QrCode.Ecc.LOW, mask=best_mask)

        scale = 10   
        border = 4    
        qr_size = qr.get_size()
        img_size = (qr_size + border * 2) * scale

        img = Image.new("RGB", (img_size, img_size), "white")
        pixels = img.load()

        for y in range(qr_size):
            for x in range(qr_size):
                if qr.get_module(x, y):  # Modul hitam
                    for dy in range(scale):
                        for dx in range(scale):
                            px = (x + border) * scale + dx
                            py = (y + border) * scale + dy
                            pixels[px, py] = (0, 0, 0)

        # img.save("qr_hello_nayuki.png")
        rawBytes = io.BytesIO()
        img.save(rawBytes, "PNG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        return img_base64