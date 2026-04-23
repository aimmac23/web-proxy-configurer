FROM debian:trixie-slim

ADD dist/app/_internal _internal
ADD dist/app/app .

CMD ["./app"]
EXPOSE 5000
