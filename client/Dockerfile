FROM oven/bun

WORKDIR /app

COPY package.json bun.lockb /app/
RUN bun install --no-cache --frozen-lockfile

CMD ["bun", "run", "dev", "--host"]
