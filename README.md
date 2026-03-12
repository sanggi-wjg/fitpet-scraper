# FitPet Scraper



## Docker

### Docker hub

```shell
docker login

# buildx 활성화 (한 번만 실행)
docker buildx create --use --bootstrap --name multiarch1
docker buildx ls

docker buildx build --platform=linux/amd64,linux/arm64 --target web    -t girr311/fitpet-scraper:web    . --push
#docker buildx build --platform=linux/amd64,linux/arm64 --target worker -t girr311/fitpet-scraper:worker . --push
#docker buildx build --platform=linux/amd64,linux/arm64 --target beat   -t girr311/fitpet-scraper:beat   . --push
```

### ECR

```shell
aws ecr get-login-password --region ap-northeast-2 --profile {{MY_PROFILE}} | docker login --username AWS --password-stdin {{MY_REPO_ID}}.dkr.ecr.ap-northeast-2.amazonaws.com

docker buildx build --platform=linux/arm64 --target web    -t {{MY_REPO_ID}}.dkr.ecr.ap-northeast-2.amazonaws.com/fitpet/scraper:web .    --push
docker buildx build --platform=linux/arm64 --target worker -t {{MY_REPO_ID}}.dkr.ecr.ap-northeast-2.amazonaws.com/fitpet/scraper:worker . --push
docker buildx build --platform=linux/arm64 --target beat   -t {{MY_REPO_ID}}.dkr.ecr.ap-northeast-2.amazonaws.com/fitpet/scraper:beat .   --push
```