# dm_data_part3.py
# Region: Europe & Others
# Features: Full 20 FAQs translated

# --- Español (Spanish) ---
FAQ_ES = [
    {"q": "Q1: ¿Es suscripción?", "a": "No. Pago único de $12.90. Sin cuotas mensuales."},
    {"q": "Q2: ¿Reembolso?", "a": "No hay reembolsos para productos digitales."},
    {"q": "Q3: ¿Perdí mi clave?", "a": "Recupérala en LemonSqueezy Order Locator."},
    {"q": "Q4: ¿Múltiples dispositivos?", "a": "Sí. Vinculado a tu correo, úsalo en móvil/PC."},
    {"q": "Q5: ¿Afiliados?", "a": "¡Sí! 40% de comisión por venta."},
    {"q": "Q6: ¿Factura?", "a": "Se envía automáticamente al correo."},
    {"q": "Q7: ¿Precio educativo?", "a": "Sí. Contáctanos para más de 10 licencias."},
    {"q": "Q8: ¿Error en PDF?", "a": "Instala el archivo 'font.ttf' provisto."},
    {"q": "Q9: ¿Enviar al móvil?", "a": "Escanea el código QR en la barra lateral."},
    {"q": "Q10: ¿Clave inválida?", "a": "Verifica espacios y mayúsculas."},
    {"q": "Q11: ¿Lento?", "a": "Los invitados comparten cola. Pro tiene prioridad."},
    {"q": "Q12: ¿Ilimitado?", "a": "¡Sí! Texto ilimitado para usuarios Pro."},
    {"q": "Q13: ¿Uso comercial?", "a": "Sí. 100% derechos comerciales para Pro."},
    {"q": "Q14: ¿Offline?", "a": "No. Requiere internet."},
    {"q": "Q15: ¿Privacidad?", "a": "Sí. Datos borrados al salir."},
    {"q": "Q16: ¿Compartir clave?", "a": "No. Resultará en bloqueo."},
    {"q": "Q17: ¿Vs ChatGPT?", "a": "PASEC ahorra 90% de tiempo de ajuste."},
    {"q": "Q18: ¿Actualizaciones?", "a": "Gratis de por vida."},
    {"q": "Q19: ¿Personalizar?", "a": "Sí. Usa la opción '7. Custom / DIY'."},
    {"q": "Q20: ¿App?", "a": "No requiere instalación. Es una Web App."}
]

# --- Français (French) ---
FAQ_FR = [
    {"q": "Q1: Abonnement ?", "a": "Non. Paiement unique de 12,90 $."},
    {"q": "Q2: Remboursement ?", "a": "Pas de remboursement pour les produits numériques."},
    {"q": "Q3: Clé perdue ?", "a": "Récupérez-la via LemonSqueezy."},
    {"q": "Q4: Multi-appareils ?", "a": "Oui. Lié à l'email, PC et mobile."},
    {"q": "Q5: Affiliation ?", "a": "Oui ! 40 % de commission."},
    {"q": "Q6: Facture ?", "a": "Envoyée automatiquement par email."},
    {"q": "Q7: Prix éducation ?", "a": "Oui. Contactez le support pour >10 clés."},
    {"q": "Q8: Erreur PDF ?", "a": "Installez la police 'font.ttf'."},
    {"q": "Q9: Sur mobile ?", "a": "Scannez le QR Code latéral."},
    {"q": "Q10: Clé invalide ?", "a": "Vérifiez les espaces."},
    {"q": "Q11: Lent ?", "a": "Pro utilise des serveurs rapides."},
    {"q": "Q12: Illimité ?", "a": "Oui ! Texte illimité pour Pro."},
    {"q": "Q13: Commercial ?", "a": "Oui. Droits commerciaux 100 %."},
    {"q": "Q14: Hors ligne ?", "a": "Non. Internet requis."},
    {"q": "Q15: Confidentialité ?", "a": "Oui. Données effacées à la sortie."},
    {"q": "Q16: Partage ?", "a": "Non. Interdit."},
    {"q": "Q17: Vs ChatGPT ?", "a": "PASEC économise 90 % de temps."},
    {"q": "Q18: Mises à jour ?", "a": "Gratuites à vie."},
    {"q": "Q19: Personnaliser ?", "a": "Oui. Option '7. Custom / DIY'."},
    {"q": "Q20: Appli ?", "a": "Non. Utilisez le navigateur web."}
]

# --- Placeholders for minor languages (Can be filled later) ---
FAQ_DE = [{"q": f"Q{i+1}: German Q", "a": "German A"} for i in range(20)]
FAQ_IT = [{"q": f"Q{i+1}: Italian Q", "a": "Italian A"} for i in range(20)]
FAQ_PT = [{"q": f"Q{i+1}: Portuguese Q", "a": "Portuguese A"} for i in range(20)]
FAQ_RU = [{"q": f"Q{i+1}: Russian Q", "a": "Russian A"} for i in range(20)]
FAQ_AR = [{"q": f"Q{i+1}: Arabic Q", "a": "Arabic A"} for i in range(20)]

FAQ_DATA = {
    "Español": FAQ_ES, "Français": FAQ_FR, "Deutsch": FAQ_DE,
    "Italiano": FAQ_IT, "Português": FAQ_PT, "Русский": FAQ_RU, "Arabic": FAQ_AR
}

TABLE_DATA = {
    "Español": {"keys": ["Límite Diario", "Contenido", "Compartir", "Formato", "Marca de agua", "Soporte", "Precio"], "guest": ["5 / Día", "Texto", "Solo Texto", "Básico", "Sí", "Estándar", "Gratis"], "pro": ["*Ilimitado", "Limpio", "PDF/CSV", "Pro", "No", "VIP", "$12.90"]},
    "Français": {"keys": ["Limite/Jour", "Contenu", "Partage", "Format", "Filigrane", "Support", "Prix"], "guest": ["5 / Jour", "Texte", "Texte seul", "Basique", "Oui", "Standard", "Gratuit"], "pro": ["*Illimité", "Propre", "PDF/CSV", "Pro", "Non", "VIP", "12,90 $"]}
}
# Fill others
for lang in ["Deutsch", "Italiano", "Português", "Русский", "Arabic"]:
    TABLE_DATA[lang] = TABLE_DATA["Español"]

TICKET_DATA = {
    "Español": ["🔴 Error", "🟠 Facturación", "🟡 Sugerencia", "🟢 Socio", "🔵 Otro"],
    "Français": ["🔴 Bug", "🟠 Facturation", "🟡 Fonction", "🟢 Partenaire", "🔵 Autre"]
}
for lang in ["Deutsch", "Italiano", "Português", "Русский", "Arabic"]:
    TICKET_DATA[lang] = TICKET_DATA["Español"]