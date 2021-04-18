import React, { useEffect, useState } from "react";
import { Container, ButtonGroup, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/LanguageList.module.css";

export default function LanguageList() {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    function getLanguages() {
      fetch("/api/languages")
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setLanguages([...data.data.languages]);
        });
    }
    getLanguages();
  }, []);

  return (
    <>
      <Container className={styles.container}>
        <p className={styles.heading}>Choose a language</p>
        <Container className={styles.langlist}>
          <ButtonGroup vertical>
            {languages.map((lang, key) => {
              return (
                <Button key={key} variant="light">
                  <Link className="langtext" to={`/${lang}`}>
                    {lang}
                  </Link>
                </Button>
              );
            })}
          </ButtonGroup>
        </Container>
      </Container>
    </>
  );
}
