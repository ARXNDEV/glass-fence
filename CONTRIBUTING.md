# Contributing to Glass Fence

Thank you for your interest in contributing to Glass Fence!

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Go 1.21+
- Node.js 18+ & npm
- Python 3.11+

### Building Locally

```bash
# Clone the repository
git clone https://github.com/arxndev/glass-fence.git
cd glass-fence

# Build all images
./build

# Or build specific components:
cd client && npm install && npm run build
cd server && go build -o bin/glass-fence cmd/glass-fence/main.go
cd ai-engine && pip install -r requirements.txt && uvicorn main:app --reload
```

### Running the Frontend in Dev Mode

```bash
cd client
cp .env.example .env.development.local
npm install
npm run serve
```

### Running the AI Engine Locally

```bash
cd ai-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running the Full Stack

```bash
cp .env.example .env
# Edit .env with your values
docker compose up -d
```

## Code Style

| Language   | Formatter / Linter         |
|------------|---------------------------|
| Go         | `gofmt`                   |
| TypeScript | `eslint` + `prettier`     |
| Python     | `black` + `ruff`          |
| SCSS       | Follow existing patterns  |

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new feature`
- `fix: resolve bug`
- `chore: update dependencies`
- `docs: update documentation`

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. Ensure your code passes all linters and tests.
3. Update documentation if you change any public API.
4. Submit a PR with a clear description.

## License

By contributing, you agree that your contributions will be licensed under the project's existing license.
