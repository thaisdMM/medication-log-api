import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "./App.tsx";

test("shows the page title as a heading", () => {
  render(<App />);

  expect(
    screen.getByRole("heading", { name: "Medication Log" }),
  ).toBeInTheDocument();
});

test("shows the medication image with its description", () => {
  render(<App />);

  expect(
    screen.getByRole("img", { name: "A medication capsule" }),
  ).toBeInTheDocument();
});
