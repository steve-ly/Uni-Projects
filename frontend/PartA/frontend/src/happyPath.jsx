import { cy } from 'cypress';

describe('admin happy path', () => {
  it('Route to register sucessfully', () => {
    cy.visit('localhost:3000/Register');
    cy.url().should('include', 'localhost:3000/Register');
  });
  it('should register sucessfully', () => {
    cy.get('#formName').type('hello')
    cy.get('#formEmail').type('hello@unsw.email')
    cy.get('#formPassword').type('123')
    cy.get('button[type="signin"]')
      .click();
  })
  it('Creates a new game successfully', () => {
    cy.contains('button', 'New Game').click()
    cy.get('#formPassword').type('123')
    cy.get('button', 'Make it')
      .click();
    cy.contains('div', '123').should('exist');
  })
  it('should start game sucessfully', () => {
    cy.contains('button', 'Start Game').click()
    cy.contains('button', 'Go to Game').click()
    cy.url().should('include', 'localhost:3000/Results');
  })
  it('should stop game sucessfully and loads results', () => {
    cy.contains('button', 'Stop Game').click()
    cy.contains('div', 'Leaderboard').should('exist');
  })
  it('should logout sucessfully', () => {
    cy.contains('button', 'Logout').click()
    cy.url().should('include', 'localhost:3000/login');
  })
  it('should login sucessfully', () => {
    cy.get('#formEmail').type('hello@unsw.email')
    cy.get('#formPassword').type('123')
    cy.get('button[type="submit"]')
      .click();
  })
});
