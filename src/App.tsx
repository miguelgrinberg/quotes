import React, { useRef, useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

interface Quote {
  id: string;
  quote: string;
  author: string;
  tags: string[];
  score: number;
};

interface FilterProps {
  tag: string;
  count: number;
};

export default function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState<string>('');
  const [filters, setFilters] = useState<FilterProps[]>([{tag: 'baz', count: 56}, {tag: 'qux', count: 44}]);
  const [tags, setTags] = useState<FilterProps[] | null>([{tag: 'foo', count: 23}, {tag: 'bar', count: 19}]);
  const [results, setResults] = useState<Quote[] | null>(null);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.value = query;
    }
  }, [query]);
    
  const onSearch = (ev: React.FormEvent) => {
    ev.preventDefault();
    setQuery(inputRef.current?.value || '');
  };
    
  const onReset = () => {
    setQuery('');
    setFilters([]);
    setTags(null);
    setResults(null);
    inputRef.current?.focus();
  };

  const onFilter = ({tag, count}: FilterProps) => {
    setFilters([...filters, {tag, count}]);
    setTags(null);
    setResults(null);
  };

  useEffect(() => {
    (async () => {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query, filters: filters.map(filter => filter.tag)}),
      });
      const data = await response.json();
      setResults(data.quotes);
      setTags(data.tags);
    })()
  }, [query, filters]);

  return (
    <Container fluid="md" className="App">
      <Row>
        <h1>Elasticsearch Vector Search Demo</h1>
        <Form onSubmit={onSearch} className="SearchForm">
          <Form.Control type="text" placeholder="Search for... ?" ref={inputRef} autoFocus={true} />
        </Form>
      </Row>
      <Row>
        <Col md={3} className="Tags">
          <>
            {filters != null && (
              <>
                {filters.map(({tag, count}) => (
                  <div key={tag} className="Filter">
                    » {tag} ({count})
                  </div>
                ))}
                {(filters.length > 0) && (
                  <>
                    <Button variant="link" onClick={onReset}>Reset</Button>
                    <hr />
                  </>
                )}
              </>
            )}
            {(tags === null) ?
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            :
              <>
                {(tags.length === 0) ?
                  <p>No tags.</p>
                :
                  <>
                    {tags.map(({tag, count}) => (
                      <div key={tag} className="Tag">
                        <Button variant="link" onClick={() => onFilter({tag, count})}>{tag}</Button> ({count})
                      </div>
                    ))}
                  </>
                }
              </>
            }
          </>
        </Col>
        <Col md={9} className="Results">
          {(results === null) ?
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          :
            <>
              {(results.length === 0) ?
                <p>No results. Sorry!</p>
              :
                <>
                  {results.map(({quote, author, score, tags}, index) => (
                    <div key={index} className="Result">
                      <p>
                        <span className="ResultQuote">{quote}</span> — <span className="ResultAuthor">{author}</span>
                        <br />
                        <span className="ResultScore">[Score: {score}]</span> <span className="ResultTags">{tags.map(tag => `#${tag}`).join(', ')}</span>
                      </p>
                    </div>
                  ))}
                </>
              }
            </>
          }
        </Col>
      </Row>
    </Container>
  );
}
