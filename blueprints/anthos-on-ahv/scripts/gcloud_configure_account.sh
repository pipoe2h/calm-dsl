account=@@{CRED_GCLOUD.username}@@
secret='@@{CRED_GCLOUD.secret}@@'

# ============== DO NO CHANGE AFTER THIS ===============

tmpfile=$(mktemp /tmp/gcloud-anthos.XXXXXX)
exec 3>"$tmpfile"
echo "$secret" >&3
exec 3>&-

project_id=$(grep project_id $tmpfile | awk -F'"' '{print $4}')
gcloud auth activate-service-account $account --key-file=$tmpfile --project=$project_id

# rm "$tmpfile"
echo "GCP_PROJECT_ID=$project_id"
echo "GCP_KEY=$tmpfile"