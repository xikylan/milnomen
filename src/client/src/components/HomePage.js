import React from "react";
import { Container } from "react-bootstrap";
import JumboHeader from "./homepage/JumboHeader";
import LanguageList from "./homepage/LanguageList";

export default function HomePage() {
  return (
    <>
      <JumboHeader />
      <Container>
        <LanguageList />
      </Container>
    </>
  );
}
