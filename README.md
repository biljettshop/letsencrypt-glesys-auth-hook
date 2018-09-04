# letsencrypt-glesys-auth-hook
Letsencrypt GleSYS Auth Hook

letsencrypt certonly --manual --manual-auth-hook ./lgah-auth.sh --manual-cleanup-hook ./lgah-cleanup.sh --preferred-challenges dns -d DOMAIN,DOMAINALIAS
