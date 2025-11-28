# Testing Checklist

Use this checklist to systematically test the Treasure Hunt Analyzer system.

## Pre-Testing Setup

- [ ] Docker and Docker Compose installed
- [ ] Sample test files available (4C alerts, SoDA reports)
- [ ] Backend .env file configured
- [ ] Frontend .env file configured (optional)

## 1. System Startup Testing

### Docker Compose
- [ ] Run `docker-compose up -d`
- [ ] Verify all containers start successfully
  ```bash
  docker-compose ps
  ```
- [ ] Check container logs for errors
  ```bash
  docker-compose logs backend
  docker-compose logs frontend
  docker-compose logs postgres
  ```

### Database Initialization
- [ ] Run database initialization
  ```bash
  docker-compose exec backend python -m app.utils.init_db
  ```
- [ ] Verify focus areas are created (should see 6)
- [ ] Verify issue types are created

### Health Checks
- [ ] Backend health endpoint responds
  ```bash
  curl http://localhost:3011/health
  ```
- [ ] Frontend loads at http://localhost:3010
- [ ] API docs accessible at http://localhost:3011/docs

## 2. Backend API Testing

### File Upload Endpoint
- [ ] Upload 4C alert Excel file
  ```bash
  curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
    -F "file=@path/to/4c-alert.xlsx"
  ```
- [ ] Verify response contains `data_source_id`
- [ ] Verify file is saved to storage
- [ ] Upload SoDA report Excel file
- [ ] Upload PDF file (if available)
- [ ] Upload CSV file (if available)
- [ ] Upload DOCX file (if available)
- [ ] Test error handling (invalid file, missing file)

### Data Source Endpoints
- [ ] List all data sources
  ```bash
  curl http://localhost:3011/api/v1/ingestion/data-sources
  ```
- [ ] Get specific data source by ID
- [ ] Verify data source metadata is correct

### Analysis Endpoints
- [ ] Run analysis on uploaded file
  ```bash
  curl -X POST "http://localhost:3011/api/v1/analysis/run" \
    -H "Content-Type: application/json" \
    -d '{"data_source_id": 1}'
  ```
- [ ] Verify analysis run is created
- [ ] List all analysis runs
- [ ] Get specific analysis run details
- [ ] Verify findings are created

### Findings Endpoint
- [ ] Get all findings
  ```bash
  curl http://localhost:3011/api/v1/analysis/findings
  ```
- [ ] Filter by focus area
  ```bash
  curl "http://localhost:3011/api/v1/analysis/findings?focus_area=ACCESS_GOVERNANCE"
  ```
- [ ] Filter by severity
- [ ] Filter by status
- [ ] Filter by date range
- [ ] Combine multiple filters

## 3. File Parser Testing

### 4C Alert Parser
- [ ] Parse 4C alert Excel file
- [ ] Verify alert metadata extracted correctly
- [ ] Verify alert records saved to database
- [ ] Check field mappings are correct
- [ ] Test with different 4C alert types

### SoDA Report Parser
- [ ] Parse SoDA report Excel file
- [ ] Verify Parameters sheet parsed
- [ ] Verify KPIs sheet parsed
- [ ] Verify Result sheet parsed
- [ ] Check report metadata extracted

### Other Parsers
- [ ] Test PDF parser (if PDF files available)
- [ ] Test CSV parser
- [ ] Test DOCX parser

## 4. Analysis Engine Testing

### Classification
- [ ] Verify findings classified into correct focus areas
- [ ] Check classification confidence scores
- [ ] Verify issue types assigned correctly
- [ ] Test with different alert types

### Risk Scoring
- [ ] Verify risk scores calculated
- [ ] Check risk levels assigned (Critical/High/Medium/Low)
- [ ] Verify risk assessments created
- [ ] Test risk score calculations are reasonable

### Money Loss Calculation
- [ ] Verify money loss calculations (if LLM configured)
- [ ] Check fallback calculations (without LLM)
- [ ] Verify confidence scores
- [ ] Test with different finding types

### Issue Grouping
- [ ] Verify findings grouped by issue type
- [ ] Check aggregated risk scores
- [ ] Verify aggregated money loss

## 5. Frontend Testing

### Dashboard Page
- [ ] Dashboard loads without errors
- [ ] Summary cards display correct numbers
- [ ] Focus Area chart renders
- [ ] Risk Level chart renders
- [ ] Money Loss chart renders (if data available)
- [ ] Findings table displays data
- [ ] Filters work correctly
- [ ] Chart updates when filters change
- [ ] Table updates when filters change

### Upload Page
- [ ] File input accepts files
- [ ] File upload works
- [ ] Progress indicator shows
- [ ] Success message displays
- [ ] Error handling works
- [ ] Automatic analysis triggers

### Findings Page
- [ ] All findings display
- [ ] Filters work
- [ ] Table sorting works
- [ ] Table search works
- [ ] Clicking row navigates to detail
- [ ] Pagination works (if implemented)

### Finding Detail Page
- [ ] Finding details display correctly
- [ ] Risk assessment shows
- [ ] Money loss shows
- [ ] Back button works
- [ ] All fields populated correctly

### Reports Page
- [ ] Report preview shows
- [ ] PDF export works
- [ ] Excel export works
- [ ] Exported files contain correct data
- [ ] Filters affect exported data

### Navigation
- [ ] All navigation links work
- [ ] Active page highlighted
- [ ] Browser back/forward works
- [ ] Direct URL access works

## 6. Integration Testing

### Complete Workflow
- [ ] Upload file → Analysis runs → Findings appear in dashboard
- [ ] Filter findings → View detail → Export report
- [ ] Multiple file uploads → All appear in dashboard
- [ ] Analysis runs → Results persist after page refresh

### Data Consistency
- [ ] Database data matches API responses
- [ ] Frontend displays match API data
- [ ] Charts reflect actual data
- [ ] Reports match displayed data

## 7. Error Handling Testing

### Backend Errors
- [ ] Invalid file format handled gracefully
- [ ] Missing file handled
- [ ] Database errors handled
- [ ] API errors return proper status codes
- [ ] Error messages are informative

### Frontend Errors
- [ ] Network errors handled
- [ ] API errors displayed to user
- [ ] Loading states shown
- [ ] Empty states displayed
- [ ] Error boundaries work

## 8. Performance Testing

### Backend Performance
- [ ] File upload completes in reasonable time
- [ ] Analysis completes in reasonable time
- [ ] API responses are fast (< 1 second)
- [ ] Database queries optimized

### Frontend Performance
- [ ] Page loads quickly
- [ ] Charts render smoothly
- [ ] Table scrolling is smooth
- [ ] No memory leaks

## 9. Browser Compatibility

- [ ] Chrome/Edge works
- [ ] Firefox works
- [ ] Safari works (if on Mac)
- [ ] Mobile browser works (responsive)

## 10. Documentation Testing

- [ ] README instructions work
- [ ] Quick Start guide works
- [ ] Testing guide is accurate
- [ ] API documentation is complete

## Test Results Template

```
Test Date: ___________
Tester: ___________

Total Tests: ___
Passed: ___
Failed: ___
Skipped: ___

Critical Issues Found:
1. 
2. 
3. 

Notes:
```

