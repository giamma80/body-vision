#!/bin/bash
set -e

echo "🚀 Initializing BodyVision project..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
uv venv --python 3.12

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
uv pip install -e ".[dev,test]"

# Copy .env.example to .env if not exists
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file. Please update with your credentials.${NC}"
fi

# Install pre-commit hooks
echo -e "${BLUE}Installing pre-commit hooks...${NC}"
pre-commit install

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Update .env with your Supabase credentials"
echo "  2. Run 'source .venv/bin/activate' to activate the virtual environment"
echo "  3. Run 'make dev' to start the development server"
echo "  4. Visit http://localhost:8000/docs for API documentation"
