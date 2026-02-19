# Contributing to Risk Minds Calc Monte Carlo Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Help each other learn and grow

## Getting Started

### 1. Fork the Repository
Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/yourusername/sg-capital-monte-carlo.git
cd sg-capital-monte-carlo
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-new-module`
- `fix/bug-description`
- `docs/improve-documentation`
- `performance/optimize-simulations`

### 4. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Making Changes

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

### Commit Messages

Write clear, descriptive commit messages:

```
[Type] Brief description

Longer explanation of what changed and why.

- Specific change 1
- Specific change 2
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests

Example:
```
fix: Correct Monte Carlo calculation

Fixed integer-generator type error in final value calculation.
Changed from np.prod(generator) to proper compound formula:
final_values = portfolio_value * (1 + annual_returns) ** time_horizon

Fixes #123
```

## Testing

### Before Submitting

1. Test your changes locally:
```bash
streamlit run app.py
```

2. Verify all modules work:
   - Dashboard loads
   - Monte Carlo runs without errors
   - Percentile analysis displays correctly
   - Factor risk analysis works
   - Data management functions

3. Check for common issues:
   - Python syntax errors
   - Missing imports
   - Type mismatches
   - Encoding issues

### Test Scenarios

Test at least:
- Small simulations (100K)
- Large simulations (5M)
- Data upload/download
- Report generation
- Different browsers (Chrome, Firefox, Edge)

## Documentation

### Update Documentation For:
- New features
- Bug fixes
- Configuration changes
- Performance improvements

### Files to Update:
- `README_GITHUB.md` - Main documentation
- `UI_GUIDE.md` - Feature guides
- Relevant `.md` files in the project
- Code comments for complex logic
- This file (CONTRIBUTING.md)

## Pull Request Process

### 1. Update Your Branch
```bash
git fetch origin
git rebase origin/main
```

### 2. Push Your Changes
```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request
- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill in PR description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Related Issue
Fixes #(issue number)

## Testing
- [ ] Tested locally
- [ ] No errors in console
- [ ] All modules functional
- [ ] Documentation updated

## Screenshots (if applicable)
Include before/after screenshots

## Additional Notes
Any other relevant information
```

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Changes are well-tested
- [ ] Commit messages are clear
- [ ] No breaking changes
- [ ] No new dependencies without approval
- [ ] All tests pass

## Code Review Process

### We Look For:
- ✅ Code quality and style
- ✅ Documentation completeness
- ✅ Test coverage
- ✅ Performance impact
- ✅ Security considerations
- ✅ Compatibility with existing code

### Review Timeline
- Standard reviews: 3-5 business days
- Complex changes: 1-2 weeks
- Urgent fixes: 1 business day

### Feedback
- Be open to constructive criticism
- Ask questions if feedback isn't clear
- Propose alternatives if you disagree
- Keep discussions professional

## Types of Contributions

### Bug Reports
1. Use GitHub Issues
2. Include environment info
3. Provide reproducible steps
4. Share error messages/screenshots

### Feature Requests
1. Describe the feature
2. Explain the use case
3. Suggest implementation approach
4. Propose documentation updates

### Documentation Improvements
1. Fix typos/clarity issues
2. Add missing information
3. Improve examples
4. Update outdated content

### Performance Improvements
1. Include benchmarks
2. Show before/after metrics
3. Explain optimization approach
4. Ensure no functionality breaks

## Development Tips

### Debugging
```python
import streamlit as st

# Use st.write for debugging
st.write("Debug value:", variable)

# Use st.exception for error info
try:
    # your code
except Exception as e:
    st.exception(e)
```

### Testing Locally
```bash
# Clear cache
streamlit cache clear

# Run with debug logging
streamlit run app.py --logger.level=debug

# Run on specific port
streamlit run app.py --server.port 8502
```

### Performance Profiling
```python
import time

start = time.time()
# your code
end = time.time()
st.write(f"Execution time: {end - start:.2f}s")
```

## Project Structure

Keep in mind the existing structure:
```
Monte_Carlo_Simulations/
├── app.py                       # Main application
├── integration_helper.py        # Module integration
├── Monte_Carlo_SIM.py           # Simulator
├── Percentale_Report.py         # Report generation
├── factor_risk_decomposition.py # Risk analysis
├── requirements.txt
├── run_ui.bat
└── Documentation/
```

## Deployment

### Before Merging to Main
1. All tests pass
2. Documentation updated
3. No breaking changes
4. Performance acceptable
5. Code reviewed and approved

### After Merge
- Tag release on GitHub
- Update version in code
- Prepare release notes
- Deploy to production

## Questions?

- Check existing issues
- Read documentation
- Ask in PR comments
- Create a discussion

## Acknowledgments

Contributors are the backbone of this project. Thank you for helping improve Risk Minds Calc!

---

**Last Updated**: February 18, 2026
**Maintained By**: Risk Minds Calc Team
