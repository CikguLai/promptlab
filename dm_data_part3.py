# dm_data_part3.py
# Region: Europe & Others
# Features: 20 FAQs (Full Translation) & Localized Tables

# --- Español (Spanish) ---
FAQ_ES = [
    {"q": "Q1: ¿Es una suscripción?", "a": "No. Es un pago único de $12.90. Sin cuotas mensuales."},
    {"q": "Q2: ¿Cuál es la política de reembolso?", "a": "Estrictamente sin reembolsos. Es un producto digital con acceso instantáneo."},
    {"q": "Q3: Perdí mi clave de licencia.", "a": "Visite el Localizador de Pedidos de LemonSqueezy para recuperarla."},
    {"q": "Q4: ¿Puedo usarlo en múltiples dispositivos?", "a": "Sí. Su licencia está vinculada a su correo, accesible en móvil/PC."},
    {"q": "Q5: ¿Tienen programa de afiliados?", "a": "¡Sí! Gana 40% de comisión por venta. Regístrese en LemonSqueezy Affiliate Hub."},
    {"q": "Q6: ¿Dónde está mi factura?", "a": "Se envía automáticamente a su correo tras la compra por LemonSqueezy."},
    {"q": "Q7: ¿Ofrecen precios educativos/por mayor?", "a": "Sí. Para escuelas o pedidos grandes (>10 claves), contacte a support@cikgulai.com."},
    {"q": "Q8: El texto PDF sale mal/faltan caracteres.", "a": "Instale el archivo 'font.ttf' provisto o asegúrese de que su dispositivo soporte fuentes UTF-8."},
    {"q": "Q9: ¿Cómo enviar al móvil (WeChat/TikTok)?", "a": "Use la función 'Mobile Handoff': Escanee el código QR en la barra lateral para sincronizar el texto."},
    {"q": "Q10: ¿Error \"Clave inválida\"?", "a": "Asegúrese de no copiar espacios. Verifique su correo. La clave distingue mayúsculas."},
    {"q": "Q11: ¿Por qué la generación es lenta?", "a": "Los invitados comparten cola. Los usuarios PRO disfrutan de servidores dedicados de alta velocidad."},
    {"q": "Q12: ¿Es PRO realmente ilimitado?", "a": "¡Sí! Al ser una IA de texto, los usuarios PRO disfrutan de generación ilimitada."},
    {"q": "Q13: ¿Puedo usar el contenido comercialmente?", "a": "Sí, los usuarios PRO tienen 100% de derechos comerciales."},
    {"q": "Q14: ¿Funciona sin conexión?", "a": "No. PromptLab es un motor de IA en la nube y requiere internet."},
    {"q": "Q15: ¿Son privados mis datos?", "a": "Sí. No almacenamos sus entradas/salidas permanentemente. Los datos se borran al salir."},
    {"q": "Q16: ¿Puedo compartir mi clave?", "a": "No. Compartir claves públicamente puede llevar a una prohibición automática."},
    {"q": "Q17: ¿Por qué comprar esto si tengo ChatGPT?", "a": "ChatGPT es el motor; nosotros somos el volante. PASEC estructura los prompts profesionalmente, ahorrando 90% de tiempo."},
    {"q": "Q18: ¿Pago por futuras actualizaciones?", "a": "No. El pago único otorga acceso de por vida a la versión actual. Las actualizaciones en la nube suelen ser gratis."},
    {"q": "Q19: ¿Puedo personalizar roles?", "a": "Sí. Use la opción '7. Custom / DIY' en el menú para ingresar sus necesidades."},
    {"q": "Q20: ¿Hay App móvil?", "a": "No requiere descarga. Es una Web App. Simplemente abra el enlace en su navegador móvil."}
]

# --- Français (French) ---
FAQ_FR = [
    {"q": "Q1: Est-ce un abonnement ?", "a": "Non. Paiement unique de 12,90 $. Pas de frais mensuels."},
    {"q": "Q2: Quelle est la politique de remboursement ?", "a": "Strictement aucun remboursement. C'est un produit numérique à accès instantané."},
    {"q": "Q3: J'ai perdu ma clé de licence.", "a": "Visitez le localisateur de commande LemonSqueezy pour la récupérer."},
    {"q": "Q4: Puis-je l'utiliser sur plusieurs appareils ?", "a": "Oui. Votre licence est liée à votre email, accessible sur mobile/PC."},
    {"q": "Q5: Avez-vous un programme d'affiliation ?", "a": "Oui ! Gagnez 40 % de commission par vente. Inscrivez-vous via LemonSqueezy."},
    {"q": "Q6: Où est ma facture ?", "a": "Elle est envoyée automatiquement par email après l'achat."},
    {"q": "Q7: Prix éducation/gros volume ?", "a": "Oui. Pour les écoles ou >10 clés, contactez support@cikgulai.com."},
    {"q": "Q8: Texte PDF illisible ?", "a": "Installez le fichier 'font.ttf' fourni ou vérifiez le support UTF-8."},
    {"q": "Q9: Comment envoyer sur mobile ?", "a": "Utilisez 'Mobile Handoff' : Scannez le QR Code latéral pour synchroniser le texte."},
    {"q": "Q10: Erreur \"Clé invalide\" ?", "a": "Vérifiez les espaces et l'email. La clé est sensible à la casse."},
    {"q": "Q11: Pourquoi est-ce lent ?", "a": "Les invités partagent la file. Les PRO ont des serveurs dédiés rapides."},
    {"q": "Q12: PRO est-il vraiment illimité ?", "a": "Oui ! En tant qu'IA textuelle, les utilisateurs PRO ont une génération illimitée."},
    {"q": "Q13: Puis-je l'utiliser commercialement ?", "a": "Oui, les utilisateurs PRO ont 100 % des droits commerciaux."},
    {"q": "Q14: Fonctionne-t-il hors ligne ?", "a": "Non. PromptLab est une IA cloud et nécessite internet."},
    {"q": "Q15: Mes données sont-elles privées ?", "a": "Oui. Pas de stockage permanent. Données effacées à la déconnexion."},
    {"q": "Q16: Puis-je partager ma clé ?", "a": "Non. Le partage public peut entraîner un bannissement automatique."},
    {"q": "Q17: Pourquoi acheter si j'ai ChatGPT ?", "a": "ChatGPT est le moteur ; nous sommes le volant. PASEC structure les prompts, économisant 90 % de temps."},
    {"q": "Q18: Payer pour les mises à jour ?", "a": "Non. Paiement unique pour un accès à vie à la version actuelle."},
    {"q": "Q19: Puis-je personnaliser les rôles ?", "a": "Oui. Utilisez l'option '7. Custom / DIY' pour vos besoins."},
    {"q": "Q20: Y a-t-il une application mobile ?", "a": "Pas de téléchargement. C'est une Web App. Ouvrez le lien sur navigateur."}
]

# --- Deutsch (German) ---
FAQ_DE = [
    {"q": "Q1: Ist das ein Abo?", "a": "Nein. Einmalzahlung von $12.90. Keine monatlichen Gebühren."},
    {"q": "Q2: Rückerstattungsrichtlinie?", "a": "Keine Rückerstattung. Dies ist ein digitales Produkt mit Sofortzugriff."},
    {"q": "Q3: Lizenzschlüssel verloren.", "a": "Besuchen Sie den LemonSqueezy Order Locator zur Wiederherstellung."},
    {"q": "Q4: Mehrere Geräte?", "a": "Ja. Lizenz ist an E-Mail gebunden, nutzbar auf Handy/PC."},
    {"q": "Q5: Partnerprogramm?", "a": "Ja! 40% Provision pro Verkauf. Anmeldung über LemonSqueezy."},
    {"q": "Q6: Wo ist meine Rechnung?", "a": "Wird nach Kauf automatisch per E-Mail gesendet."},
    {"q": "Q7: Bildungs-/Mengenrabatt?", "a": "Ja. Für Schulen oder >10 Schlüssel, kontaktieren Sie support@cikgulai.com."},
    {"q": "Q8: PDF-Text fehlerhaft?", "a": "Installieren Sie 'font.ttf' oder prüfen Sie UTF-8-Support."},
    {"q": "Q9: An Handy senden?", "a": "Nutzen Sie 'Mobile Handoff': QR-Code in der Seitenleiste scannen."},
    {"q": "Q10: Fehler 'Ungültiger Schlüssel'?", "a": "Keine Leerzeichen kopieren. E-Mail prüfen. Groß-/Kleinschreibung beachten."},
    {"q": "Q11: Warum langsam?", "a": "Gäste teilen sich Warteschlange. PRO nutzt dedizierte High-Speed-Server."},
    {"q": "Q12: Wirklich unbegrenzt?", "a": "Ja! PRO-Nutzer haben unbegrenzte Textgenerierung."},
    {"q": "Q13: Kommerzielle Nutzung?", "a": "Ja, PRO-Nutzer haben 100% kommerzielle Rechte."},
    {"q": "Q14: Offline nutzbar?", "a": "Nein. Benötigt Internetverbindung."},
    {"q": "Q15: Datenschutz?", "a": "Ja. Keine dauerhafte Speicherung. Daten werden beim Logout gelöscht."},
    {"q": "Q16: Schlüssel teilen?", "a": "Nein. Öffentliches Teilen führt zur Sperrung."},
    {"q": "Q17: Warum kaufen trotz ChatGPT?", "a": "ChatGPT ist der Motor, wir das Lenkrad. PASEC spart 90% Zeit."},
    {"q": "Q18: Kosten Updates?", "a": "Nein. Einmalzahlung für lebenslangen Zugriff auf aktuelle Version."},
    {"q": "Q19: Rollen anpassen?", "a": "Ja. Nutzen Sie '7. Custom / DIY' im Menü."},
    {"q": "Q20: Mobile App?", "a": "Kein Download nötig. Web App im Browser öffnen."}
]

# --- Italiano (Italian) ---
FAQ_IT = [
    {"q": "Q1: È un abbonamento?", "a": "No. Pagamento unico di $12.90. Nessun canone mensile."},
    {"q": "Q2: Rimborso?", "a": "Nessun rimborso. Prodotto digitale ad accesso immediato."},
    {"q": "Q3: Chiave persa.", "a": "Usa LemonSqueezy Order Locator per recuperarla."},
    {"q": "Q4: Più dispositivi?", "a": "Sì. Legato alla mail, accessibile su mobile/PC."},
    {"q": "Q5: Affiliazione?", "a": "Sì! 40% di commissione. Iscriviti su LemonSqueezy."},
    {"q": "Q6: Fattura?", "a": "Inviata automaticamente via email."},
    {"q": "Q7: Sconto scuole?", "a": "Sì. Per >10 chiavi contattare support@cikgulai.com."},
    {"q": "Q8: Errore PDF?", "a": "Installa 'font.ttf' fornito."},
    {"q": "Q9: Inviare al cellulare?", "a": "Scansiona il QR Code nella barra laterale."},
    {"q": "Q10: Chiave non valida?", "a": "Controlla spazi e maiuscole."},
    {"q": "Q11: Lento?", "a": "Guest condivisi. PRO ha server dedicati."},
    {"q": "Q12: Illimitato?", "a": "Sì! Generazione testo illimitata per PRO."},
    {"q": "Q13: Uso commerciale?", "a": "Sì, 100% diritti commerciali per PRO."},
    {"q": "Q14: Offline?", "a": "No. Serve internet."},
    {"q": "Q15: Privacy?", "a": "Sì. Dati cancellati al logout."},
    {"q": "Q16: Condividere chiave?", "a": "No. Rischio ban."},
    {"q": "Q17: Vs ChatGPT?", "a": "PASEC struttura i prompt, risparmiando il 90% del tempo."},
    {"q": "Q18: Aggiornamenti pagati?", "a": "No. Accesso a vita alla versione attuale."},
    {"q": "Q19: Personalizzare?", "a": "Sì. Usa '7. Custom / DIY'."},
    {"q": "Q20: App mobile?", "a": "No. È una Web App."}
]

# --- Português (Portuguese) ---
FAQ_PT = [
    {"q": "Q1: É assinatura?", "a": "Não. Pagamento único de $12.90. Sem mensalidade."},
    {"q": "Q2: Reembolso?", "a": "Sem reembolso. Produto digital de acesso imediato."},
    {"q": "Q3: Perdi a chave.", "a": "Use o LemonSqueezy Order Locator."},
    {"q": "Q4: Múltiplos dispositivos?", "a": "Sim. Vinculado ao email, usa no celular/PC."},
    {"q": "Q5: Afiliados?", "a": "Sim! 40% de comissão. Cadastre no LemonSqueezy."},
    {"q": "Q6: Fatura?", "a": "Enviada automaticamente por email."},
    {"q": "Q7: Preço educacional?", "a": "Sim. Para >10 chaves, contate suporte."},
    {"q": "Q8: Erro no PDF?", "a": "Instale 'font.ttf' fornecido."},
    {"q": "Q9: Enviar pro celular?", "a": "Escaneie o QR Code na barra lateral."},
    {"q": "Q10: Chave inválida?", "a": "Verifique espaços e maiúsculas."},
    {"q": "Q11: Lento?", "a": "Guest compartilha fila. PRO tem servidor rápido."},
    {"q": "Q12: Ilimitado?", "a": "Sim! Geração de texto ilimitada para PRO."},
    {"q": "Q13: Uso comercial?", "a": "Sim. 100% direitos comerciais para PRO."},
    {"q": "Q14: Offline?", "a": "Não. Requer internet."},
    {"q": "Q15: Privacidade?", "a": "Sim. Dados apagados ao sair."},
    {"q": "Q16: Compartilhar chave?", "a": "Não. Pode causar banimento."},
    {"q": "Q17: Vs ChatGPT?", "a": "PASEC estrutura prompts, economizando 90% do tempo."},
    {"q": "Q18: Pagar atualizações?", "a": "Não. Acesso vitalício à versão atual."},
    {"q": "Q19: Personalizar?", "a": "Sim. Use '7. Custom / DIY'."},
    {"q": "Q20: App móvel?", "a": "Não. É um Web App."}
]

# --- Русский (Russian) ---
FAQ_RU = [
    {"q": "Q1: Это подписка?", "a": "Нет. Разовый платеж $12.90. Без ежемесячной платы."},
    {"q": "Q2: Возврат средств?", "a": "Возврата нет. Это цифровой продукт."},
    {"q": "Q3: Потерял ключ.", "a": "Восстановите через LemonSqueezy Order Locator."},
    {"q": "Q4: Несколько устройств?", "a": "Да. Привязано к email, работает на ПК/мобильном."},
    {"q": "Q5: Партнерка?", "a": "Да! 40% комиссии с продажи."},
    {"q": "Q6: Где чек?", "a": "Приходит на email автоматически."},
    {"q": "Q7: Скидки школам?", "a": "Да. Для >10 ключей пишите в поддержку."},
    {"q": "Q8: Ошибка PDF?", "a": "Установите 'font.ttf'."},
    {"q": "Q9: Отправить на телефон?", "a": "Сканируйте QR-код в боковой панели."},
    {"q": "Q10: Неверный ключ?", "a": "Проверьте пробелы и регистр."},
    {"q": "Q11: Медленно?", "a": "Гости в общей очереди. PRO на быстрых серверах."},
    {"q": "Q12: Безлимит?", "a": "Да! Безлимитная генерация текста для PRO."},
    {"q": "Q13: Коммерческое использование?", "a": "Да. 100% прав у PRO."},
    {"q": "Q14: Офлайн?", "a": "Нет. Нужен интернет."},
    {"q": "Q15: Приватность?", "a": "Да. Данные удаляются при выходе."},
    {"q": "Q16: Делиться ключом?", "a": "Нет. Это приведет к бану."},
    {"q": "Q17: Зачем это, если есть ChatGPT?", "a": "PASEC экономит 90% времени настройки промптов."},
    {"q": "Q18: Платные обновления?", "a": "Нет. Пожизненный доступ к версии."},
    {"q": "Q19: Свой роль?", "a": "Да. Используйте '7. Custom / DIY'."},
    {"q": "Q20: Мобильное приложение?", "a": "Нет. Работает в браузере."}
]

# --- Arabic (Arabic) ---
FAQ_AR = [
    {"q": "س1: هل هذا اشتراك؟", "a": "لا. دفعة لمرة واحدة 12.90 دولار."},
    {"q": "س2: استرداد الأموال؟", "a": "لا يوجد استرداد للمنتجات الرقمية."},
    {"q": "س3: فقدت المفتاح.", "a": "استعده عبر LemonSqueezy."},
    {"q": "س4: أجهزة متعددة؟", "a": "نعم. مرتبط بالبريد الإلكتروني."},
    {"q": "س5: برنامج التسويق؟", "a": "نعم! عمولة 40%."},
    {"q": "س6: الفاتورة؟", "a": "تصل تلقائياً عبر البريد."},
    {"q": "س7: خصم تعليمي؟", "a": "نعم. للطلبات >10 تواصل معنا."},
    {"q": "س8: خطأ PDF؟", "a": "قم بتثبيت 'font.ttf'."},
    {"q": "س9: إرسال للهاتف؟", "a": "امسح رمز QR في القائمة الجانبية."},
    {"q": "س10: مفتاح غير صالح؟", "a": "تحقق من المسافات والأحرف."},
    {"q": "س11: بطيء؟", "a": "الضيوف في طابور مشترك. PRO أسرع."},
    {"q": "س12: غير محدود؟", "a": "نعم! نصوص غير محدودة لـ PRO."},
    {"q": "س13: استخدام تجاري؟", "a": "نعم. حقوق تجارية 100%."},
    {"q": "س14: بدون نت؟", "a": "لا. يتطلب إنترنت."},
    {"q": "س15: الخصوصية؟", "a": "نعم. تحذف البيانات عند الخروج."},
    {"q": "س16: مشاركة المفتاح؟", "a": "لا. يؤدي للحظر."},
    {"q": "س17: الفرق عن ChatGPT؟", "a": "PASEC يوفر 90% من الوقت."},
    {"q": "س18: تحديثات؟", "a": "مجانية مدى الحياة."},
    {"q": "س19: تخصيص؟", "a": "نعم. اختر '7. Custom / DIY'."},
    {"q": "س20: تطبيق؟", "a": "لا. يعمل عبر المتصفح."}
]

FAQ_DATA = {
    "Español": FAQ_ES, "Français": FAQ_FR, "Deutsch": FAQ_DE,
    "Italiano": FAQ_IT, "Português": FAQ_PT, "Русский": FAQ_RU, "Arabic": FAQ_AR
}

# [LOCALIZED TABLE]
TABLE_DATA = {
    "Español": {"keys": ["Límite Diario", "Contenido", "Compartir", "Formato", "Marca de agua", "Soporte", "Precio"], "guest": ["5 / Día", "Texto", "Solo Texto", "Básico", "Sí", "Estándar", "Gratis"], "pro": ["*Ilimitado", "Limpio", "PDF/CSV", "Pro", "No", "VIP", "$12.90"]},
    "Français": {"keys": ["Limite/Jour", "Contenu", "Partage", "Format", "Filigrane", "Support", "Prix"], "guest": ["5 / Jour", "Texte", "Texte seul", "Basique", "Oui", "Standard", "Gratuit"], "pro": ["*Illimité", "Propre", "PDF/CSV", "Pro", "Non", "VIP", "12,90 $"]},
    "Deutsch": {"keys": ["Tageslimit", "Inhalt", "Teilen", "Format", "Wasserzeichen", "Support", "Preis"], "guest": ["5 / Tag", "Text", "Nur Text", "Basis", "Ja", "Standard", "Kostenlos"], "pro": ["*Unbegrenzt", "Sauber", "PDF/CSV", "Pro", "Nein", "VIP", "$12.90"]},
    "Italiano": {"keys": ["Limite/Giorno", "Contenuto", "Condivisione", "Formato", "Filigrana", "Supporto", "Prezzo"], "guest": ["5 / Giorno", "Testo", "Solo Testo", "Base", "Sì", "Standard", "Gratis"], "pro": ["*Illimitato", "Pulito", "PDF/CSV", "Pro", "No", "VIP", "$12.90"]},
    "Português": {"keys": ["Limite/Dia", "Conteúdo", "Partilha", "Formato", "Marca d'água", "Suporte", "Preço"], "guest": ["5 / Dia", "Texto", "Só Texto", "Básico", "Sim", "Padrão", "Grátis"], "pro": ["*Ilimitado", "Limpo", "PDF/CSV", "Pro", "Não", "VIP", "$12.90"]},
    "Русский": {"keys": ["Лимит/день", "Контент", "Поделиться", "Формат", "Водяной знак", "Поддержка", "Цена"], "guest": ["5 / День", "Текст", "Только текст", "База", "Да", "Стандарт", "Бесплатно"], "pro": ["*Безлимит", "Чисто", "PDF/CSV", "Pro", "Нет", "VIP", "$12.90"]},
    "Arabic": {"keys": ["حد يومي", "محتوى", "مشاركة", "صيغة", "علامة مائية", "دعم", "سعر"], "guest": ["5 / يوم", "نص", "نص فقط", "أساسي", "نعم", "عادي", "مجاني"], "pro": ["*غير محدود", "نظيف", "PDF/CSV", "Pro", "لا", "VIP", "$12.90"]}
}

TICKET_DATA = {
    "Español": ["🔴 Error", "🟠 Facturación", "🟡 Sugerencia", "🟢 Socio", "🔵 Otro"],
    "Français": ["🔴 Bug", "🟠 Facturation", "🟡 Fonction", "🟢 Partenaire", "🔵 Autre"],
    "Deutsch": ["🔴 Fehler", "🟠 Rechnung", "🟡 Feature", "🟢 Partner", "🔵 Andere"],
    "Italiano": ["🔴 Bug", "🟠 Fatturazione", "🟡 Funzione", "🟢 Partner", "🔵 Altro"],
    "Português": ["🔴 Erro", "🟠 Faturamento", "🟡 Recurso", "🟢 Parceiro", "🔵 Outro"],
    "Русский": ["🔴 Ошибка", "🟠 Оплата", "🟡 Функция", "🟢 Партнер", "🔵 Другое"],
    "Arabic": ["🔴 خطأ", "🟠 فوترة", "🟡 ميزة", "🟢 شريك", "🔵 آخر"]
}
