# dm_data.py
# Lai's Lab Data Module - FINAL COMPLETE VERSION
# Features: 16 Languages Data (FAQ, Tickets, Tables)

# ==========================================
# 1. FAQ 数据 (FAQ Database - 16 Languages)
# ==========================================
FAQ_EN = [
    {"q": "Q1: Is it a subscription?", "a": "No. One-time payment."},
    {"q": "Q2: Refund?", "a": "No refunds for digital keys."},
    {"q": "Q3: Lost Key?", "a": "Check LemonSqueezy orders."},
    {"q": "Q4: How many devices?", "a": "Multiple personal devices."},
    {"q": "Q5: Affiliate program?", "a": "Yes, 40% commission."},
    {"q": "Q6: Invoice?", "a": "Sent to email automatically."},
    {"q": "Q7: School Bulk Buy?", "a": "Contact support@cikgulai.com."},
    {"q": "Q8: PDF garbled?", "a": "Install font.ttf."},
    {"q": "Q9: Share to WeChat?", "a": "Copy and paste manually."},
    {"q": "Q10: Invalid Key?", "a": "Check spaces/case."},
    {"q": "Q11: Slow speed?", "a": "Guests share queue. Pro is fast."},
    {"q": "Q12: Truly Unlimited?", "a": "Yes, for fair use text."},
    {"q": "Q13: Commercial use?", "a": "Yes, for Pro users."},
    {"q": "Q14: Offline?", "a": "No, internet required."},
    {"q": "Q15: Privacy?", "a": "We don't store inputs."},
    {"q": "Q16: Share account?", "a": "No, may lead to ban."}
]

FAQ_CN = [
    {"q": "问1: 是订阅制吗？", "a": "不是，一次性付费。"},
    {"q": "问2: 能退款吗？", "a": "激活码发出后不可退款。"},
    {"q": "问3: 丢了码？", "a": "请去订单页找回。"},
    {"q": "问4: 设备限制？", "a": "支持个人多设备。"},
    {"q": "问5: 分销计划？", "a": "有，40% 佣金。"},
    {"q": "问6: 发票？", "a": "自动发送到邮箱。"},
    {"q": "问7: 学校团购？", "a": "请联系客服优惠。"},
    {"q": "问8: PDF乱码？", "a": "请安装 font.ttf。"},
    {"q": "问9: 分享微信？", "a": "复制后手动粘贴。"},
    {"q": "问10: 激活码无效？", "a": "检查空格和大小写。"},
    {"q": "问11: 速度慢？", "a": "Pro 拥有优先通道。"},
    {"q": "问12: 真的无限吗？", "a": "文本生成无限。"},
    {"q": "问13: 可商用吗？", "a": "Pro 用户可商用。"},
    {"q": "问14: 离线模式？", "a": "需要联网。"},
    {"q": "问15: 隐私安全？", "a": "不永久存储数据。"},
    {"q": "问16: 共享账号？", "a": "禁止，会被封号。"}
]

FAQ_TC = [
    {"q": "問1: 是訂閱制嗎？", "a": "不是，一次性付費。"},
    {"q": "問2: 能退款嗎？", "a": "激活碼發出後不可退款。"},
    {"q": "問3: 遺失激活碼？", "a": "請去訂單頁找回。"},
    {"q": "問4: 設備限制？", "a": "支持個人多設備。"},
    {"q": "問5: 分銷計劃？", "a": "有，40% 佣金。"},
    {"q": "問6: 發票？", "a": "自動發送到郵箱。"},
    {"q": "問7: 學校團購？", "a": "請聯繫客服優惠。"},
    {"q": "問8: PDF亂碼？", "a": "請安裝 font.ttf。"},
    {"q": "問9: 分享微信？", "a": "複製後手動貼上。"},
    {"q": "問10: 激活碼無效？", "a": "檢查空格和大小寫。"},
    {"q": "問11: 速度慢？", "a": "Pro 擁有優先通道。"},
    {"q": "問12: 真的無限嗎？", "a": "文本生成無限。"},
    {"q": "問13: 可商用嗎？", "a": "Pro 用戶可商用。"},
    {"q": "問14: 離線模式？", "a": "需要聯網。"},
    {"q": "問15: 隱私安全？", "a": "不永久存儲數據。"},
    {"q": "問16: 共享賬號？", "a": "禁止，會被封號。"}
]

FAQ_MY = [
    {"q": "S1: Langganan?", "a": "Tidak. Bayar sekali sahaja."},
    {"q": "S2: Bayaran balik?", "a": "Tiada untuk produk digital."},
    {"q": "S3: Kunci Hilang?", "a": "Semak LemonSqueezy."},
    {"q": "S4: Peranti?", "a": "Boleh banyak peranti."},
    {"q": "S5: Affiliate?", "a": "Ya, komisen 40%."},
    {"q": "S6: Invois?", "a": "Dihantar ke emel."},
    {"q": "S7: Belian Sekolah?", "a": "Hubungi sokongan."},
    {"q": "S8: PDF Rosak?", "a": "Pasang font.ttf."},
    {"q": "S9: Kongsi WeChat?", "a": "Salin dan tampal."},
    {"q": "S10: Kunci Salah?", "a": "Semak ruang kosong."},
    {"q": "S11: Lambat?", "a": "Tetamu kongsi, Pro laju."},
    {"q": "S12: Tanpa Had?", "a": "Ya, teks tanpa had."},
    {"q": "S13: Kegunaan Niaga?", "a": "Ya, untuk Pro."},
    {"q": "S14: Luar Talian?", "a": "Perlu internet."},
    {"q": "S15: Privasi?", "a": "Data tidak disimpan."},
    {"q": "S16: Kongsi Akaun?", "a": "Dilarang."}
]

FAQ_ES = [ # Español
    {"q": "P1: ¿Es suscripción?", "a": "No. Pago único."},
    {"q": "P2: ¿Reembolso?", "a": "No para productos digitales."},
    {"q": "P3: ¿Clave perdida?", "a": "Revisar LemonSqueezy."},
    {"q": "P4: ¿Dispositivos?", "a": "Múltiples personales."},
    {"q": "P5: ¿Afiliados?", "a": "Sí, 40% comisión."},
    {"q": "P6: ¿Factura?", "a": "Enviada al correo."},
    {"q": "P7: ¿Escuelas?", "a": "Contactar soporte."},
    {"q": "P8: ¿Error PDF?", "a": "Instalar font.ttf."},
    {"q": "P9: ¿WeChat?", "a": "Copiar y pegar."},
    {"q": "P10: ¿Clave inválida?", "a": "Revisar espacios."},
    {"q": "P11: ¿Lento?", "a": "Pro es más rápido."},
    {"q": "P12: ¿Ilimitado?", "a": "Sí, uso justo."},
    {"q": "P13: ¿Uso comercial?", "a": "Sí, para Pro."},
    {"q": "P14: ¿Offline?", "a": "No, requiere internet."},
    {"q": "P15: ¿Privacidad?", "a": "No guardamos datos."},
    {"q": "P16: ¿Compartir?", "a": "No, prohibido."}
]

FAQ_JP = [ # 日本語
    {"q": "Q1: サブスクですか？", "a": "いいえ、買い切りです。"},
    {"q": "Q2: 返金は？", "a": "デジタル商品は不可です。"},
    {"q": "Q3: キー紛失？", "a": "注文履歴を確認ください。"},
    {"q": "Q4: デバイス数？", "a": "複数台で利用可能です。"},
    {"q": "Q5: アフィリエイト？", "a": "はい、報酬40%です。"},
    {"q": "Q6: 請求書は？", "a": "メールで送信されます。"},
    {"q": "Q7: 学校導入？", "a": "サポートへ連絡ください。"},
    {"q": "Q8: PDF文字化け？", "a": "font.ttfを入れてください。"},
    {"q": "Q9: WeChat共有？", "a": "コピペしてください。"},
    {"q": "Q10: キー無効？", "a": "空白を確認してください。"},
    {"q": "Q11: 遅い？", "a": "Proは高速回線です。"},
    {"q": "Q12: 本当に無制限？", "a": "はい、テキストは無制限。"},
    {"q": "Q13: 商用利用？", "a": "Proは可能です。"},
    {"q": "Q14: オフライン？", "a": "ネットが必要です。"},
    {"q": "Q15: プライバシー？", "a": "保存しません。"},
    {"q": "Q16: アカウント共有？", "a": "禁止されています。"}
]

FAQ_KR = [ # 한국어
    {"q": "Q1: 구독형인가요?", "a": "아니요, 평생 소장입니다."},
    {"q": "Q2: 환불 되나요?", "a": "디지털 제품은 불가합니다."},
    {"q": "Q3: 키 분실?", "a": "주문 페이지 확인하세요."},
    {"q": "Q4: 기기 제한?", "a": "여러 기기 사용 가능."},
    {"q": "Q5: 파트너 제휴?", "a": "네, 수수료 40%입니다."},
    {"q": "Q6: 영수증?", "a": "이메일로 전송됩니다."},
    {"q": "Q7: 학교 구매?", "a": "고객센터 문의 바랍니다."},
    {"q": "Q8: PDF 깨짐?", "a": "font.ttf 설치하세요."},
    {"q": "Q9: 위챗 공유?", "a": "복사해서 붙여넣으세요."},
    {"q": "Q10: 키 오류?", "a": "공백을 확인하세요."},
    {"q": "Q11: 속도 느림?", "a": "Pro는 전용 서버 사용."},
    {"q": "Q12: 진짜 무제한?", "a": "네, 텍스트 무제한."},
    {"q": "Q13: 상업용?", "a": "Pro는 가능합니다."},
    {"q": "Q14: 오프라인?", "a": "인터넷 필요합니다."},
    {"q": "Q15: 개인정보?", "a": "저장하지 않습니다."},
    {"q": "Q16: 계정 공유?", "a": "금지, 차단될 수 있음."}
]

FAQ_FR = [ # Français
    {"q": "Q1: Abonnement ?", "a": "Non. Paiement unique."},
    {"q": "Q2: Remboursement ?", "a": "Non, produit numérique."},
    {"q": "Q3: Clé perdue ?", "a": "Voir LemonSqueezy."},
    {"q": "Q4: Appareils ?", "a": "Multiples personnels."},
    {"q": "Q5: Affiliation ?", "a": "Oui, 40% commission."},
    {"q": "Q6: Facture ?", "a": "Envoyée par email."},
    {"q": "Q7: Pour écoles ?", "a": "Contactez le support."},
    {"q": "Q8: Erreur PDF ?", "a": "Installez font.ttf."},
    {"q": "Q9: WeChat ?", "a": "Copier et coller."},
    {"q": "Q10: Clé invalide ?", "a": "Vérifiez les espaces."},
    {"q": "Q11: Lent ?", "a": "Pro est prioritaire."},
    {"q": "Q12: Illimité ?", "a": "Oui, usage équitable."},
    {"q": "Q13: Commercial ?", "a": "Oui, pour Pro."},
    {"q": "Q14: Hors ligne ?", "a": "Non, internet requis."},
    {"q": "Q15: Confidentialité ?", "a": "Aucun stockage."},
    {"q": "Q16: Partage ?", "a": "Non, interdit."}
]

FAQ_DE = [ # Deutsch
    {"q": "F1: Abo?", "a": "Nein. Einmalzahlung."},
    {"q": "F2: Rückerstattung?", "a": "Nein für digitale Keys."},
    {"q": "F3: Key weg?", "a": "Siehe LemonSqueezy."},
    {"q": "F4: Geräte?", "a": "Mehrere möglich."},
    {"q": "F5: Affiliate?", "a": "Ja, 40% Provision."},
    {"q": "F6: Rechnung?", "a": "Kommt per E-Mail."},
    {"q": "F7: Schulen?", "a": "Support kontaktieren."},
    {"q": "F8: PDF Fehler?", "a": "font.ttf installieren."},
    {"q": "F9: WeChat?", "a": "Kopieren und einfügen."},
    {"q": "F10: Key ungültig?", "a": "Leerzeichen prüfen."},
    {"q": "F11: Langsam?", "a": "Pro ist schneller."},
    {"q": "F12: Unbegrenzt?", "a": "Ja, Text unbegrenzt."},
    {"q": "F13: Kommerziell?", "a": "Ja, für Pro User."},
    {"q": "F14: Offline?", "a": "Nein, Internet nötig."},
    {"q": "F15: Datenschutz?", "a": "Keine Speicherung."},
    {"q": "F16: Teilen?", "a": "Verboten."}
]

FAQ_IT = [ # Italiano
    {"q": "D1: Abbonamento?", "a": "No. Pagamento unico."},
    {"q": "D2: Rimborso?", "a": "No per beni digitali."},
    {"q": "D3: Chiave persa?", "a": "Controlla LemonSqueezy."},
    {"q": "D4: Dispositivi?", "a": "Multipli personali."},
    {"q": "D5: Affiliazione?", "a": "Sì, 40% commissione."},
    {"q": "D6: Fattura?", "a": "Inviata via email."},
    {"q": "D7: Scuole?", "a": "Contatta il supporto."},
    {"q": "D8: Errore PDF?", "a": "Installa font.ttf."},
    {"q": "D9: WeChat?", "a": "Copia e incolla."},
    {"q": "D10: Chiave errata?", "a": "Controlla spazi."},
    {"q": "D11: Lento?", "a": "Pro è prioritario."},
    {"q": "D12: Illimitato?", "a": "Sì, testo illimitato."},
    {"q": "D13: Commerciale?", "a": "Sì, per Pro."},
    {"q": "D14: Offline?", "a": "No, serve internet."},
    {"q": "D15: Privacy?", "a": "Nessun salvataggio."},
    {"q": "D16: Condivisione?", "a": "Vietata."}
]

FAQ_PT = [ # Português
    {"q": "P1: Assinatura?", "a": "Não. Pagamento único."},
    {"q": "P2: Reembolso?", "a": "Não para digitais."},
    {"q": "P3: Chave perdida?", "a": "Ver LemonSqueezy."},
    {"q": "P4: Dispositivos?", "a": "Múltiplos pessoais."},
    {"q": "P5: Afiliados?", "a": "Sim, 40% comissão."},
    {"q": "P6: Fatura?", "a": "Enviada por email."},
    {"q": "P7: Escolas?", "a": "Contate suporte."},
    {"q": "P8: Erro PDF?", "a": "Instale font.ttf."},
    {"q": "P9: WeChat?", "a": "Copiar e colar."},
    {"q": "P10: Chave inválida?", "a": "Verifique espaços."},
    {"q": "P11: Lento?", "a": "Pro é rápido."},
    {"q": "P12: Ilimitado?", "a": "Sim, texto ilimitado."},
    {"q": "P13: Comercial?",
