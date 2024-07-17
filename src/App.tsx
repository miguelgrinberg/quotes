import React, { useRef, useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

interface FilterProps {
  tag: string;
  count: number;
};

export default function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState<string>('');
  const [filters, setFilters] = useState<FilterProps[]>([{tag: 'baz', count: 56}, {tag: 'qux', count: 44}]);
  const [tags, setTags] = useState<FilterProps[]>([{tag: 'foo', count: 23}, {tag: 'bar', count: 19}]);
  const [results, setResults] = useState([
    {quote: 'foo bar bar', author: 'John Doe', score: 0.67, tags: ['foo', 'bar']},
    {quote: 'foo bar bar', author: 'John Doe', score: 0.67, tags: ['foo', 'bar']},
  ]);

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
    setTags([]);
    setResults([]);
    inputRef.current?.focus();
  };

  const onFilter = ({tag, count}: FilterProps) => {
    setFilters([...filters, {tag, count}]);
    setTags([]);
    setResults([]);
  };

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
          {(tags.length === 0) ?
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          :
            <>
              {tags.map(({tag, count}) => (
                <div key={tag} className="Tag">
                  <Button variant="link" onClick={() => onFilter({tag, count})}>{tag}</Button> ({count})
                </div>
              ))}
            </>
          }
        </Col>
        <Col md={9} className="Results">
        {(results.length === 0) ?
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
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
        </Col>
      </Row>
    </Container>
  );
}
