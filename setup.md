## Getting Started

To get started, you'll need the following:

1. An IBM Cloud account.
2. Watson AI services on the IBM Cloud platform.
3. Access to AWS SageMaker.

### Setting up the IBM Cloud and Watson AI

1. Create an account on [IBM Cloud](https://cloud.ibm.com/).

   - Go to the IBM Cloud website and click on "Sign up" to create a new account.
   - Follow the on-screen instructions to set up your account.

2. Once you have your IBM Cloud account, log in to your account [here](https://cloud.ibm.com/iam/apikeys).

   - On this page, click on "Create" to create a new API key.
   - Copy the generated API key.

3. In the project directory, create a `.env` file and add the following line:

   ```plaintext
   API_KEY=<your_ibm_cloud_api_key>
   ```

   - Replace `<your_ibm_cloud_api_key>` with the API key you copied earlier.

4. Additionally, we need to add the `PROJECT_ID` to the `.env` file.

   - Go to your IBM Cloud account, navigate to your project, and click on "Manage".
   - Copy the `Project ID` value.

   ```plaintext
   PROJECT_ID=<your_watsonx_project_id>
   ```

   - Replace `<your_watsonx_project_id>` with your actual WatsonX project ID.

### Setting up AWS SageMaker

1. Create an account on [AWS](https://aws.amazon.com/).

   - Go to the AWS website and click on "Create an AWS Account" to create a new account.
   - Follow the on-screen instructions to set up your account.

2. Once you have an AWS account, follow these steps to create an AWS SageMaker notebook instance:

   - Sign in to the AWS Management Console and open the SageMaker console.
   - In the sidebar, click on "Notebook instances".
   - Click on the "Create notebook instance" button.
   - Provide a name for your notebook instance.
   - Choose an instance type that has GPU support. This is important for running the required deep learning models.
   - (Optional) Customize other settings such as storage volume size, IAM role, etc.
   - Click on "Create notebook instance" to create the instance.

3. Once the notebook instance is created, click on "Open JupyterLab" to open the JupyterLab interface.

   - This will open a new tab in your web browser containing the JupyterLab interface.

### Building the project

1. In the JupyterLab interface, click on the "Terminal" tab to open a terminal.

   - This will open a terminal within the JupyterLab interface.

2. In the terminal, run the following commands to create a Python environment:

   ```bash
   conda create -n myenv python=3.10
   conda activate myenv
   ```

   - These commands create a new Python environment named "myenv" with Python version 3.10 and activate it.

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   - This command installs all the necessary Python packages and libraries required for the project.

4. Clone the repository:

   ```bash
   git clone https://github.ibm.com/ruslanmv/GenAI-3DVR.git
   ```

   - This command clones the project repository to your local machine.

5. Run the application:

   ```bash
   python app.py
   ```

   - This command starts the application and runs the Gradio interface.

6. In the terminal, you will see a link displayed. Copy and paste this link into your web browser.

   - The link will typically be something like `http://localhost:5000`.

7. The Gradio interface will be launched in your web browser.

   - You can now interact with the interface, enter your prompt, and generate 360° images.

8. Additionally, a Gradio shared link will be displayed in the terminal.

   - This link can be shared with others to access the Gradio interface online without running the code locally.

Please note that you need to replace `<your_ibm_cloud_api_key>` and `<your_watsonx_project_id>` with your actual credentials obtained from the IBM Cloud and Watson AI services.