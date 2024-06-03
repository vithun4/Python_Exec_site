const API_URL = 'http://localhost:8000';

// Corrected testCode function
export const testCode = async (code:string) => {
  try {
    const response = await fetch(`${API_URL}/test-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return errorData.detail;
    }

    return response.json();
  } catch (error) {
    console.error('Error testing code:', error);
    throw error;
  }
};

export const submitCode = async (code:string) => {
  try {
    const response = await fetch(`${API_URL}/submit-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return errorData.detail;
    }

    return response.json();
  } catch (error) {
    console.error('Error submitting code:', error);
    throw error;
  }
};
