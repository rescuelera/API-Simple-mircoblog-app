
node{
    stage("Create folder"){
        sh 'mkdir -p ${BUILD_ID}'
    }
    stage("Run tests"){
        withDockerContainer(args: '-u root -e API_HOST='+API_HOST+'', image: 'python:3.9') {
            sh 'git clone https://github.com/rescuelera/API-Simple-mircoblog-app.git ./${BUILD_ID}/API-Simple-mircoblog-app'
            sh 'ls -las ./${BUILD_ID}/API-Simple-mircoblog-app'
            sh 'cd ./${BUILD_ID}/API-Simple-mircoblog-app && pip install -r requirements.txt'
            sh 'cd ./${BUILD_ID}/API-Simple-mircoblog-app && pytest tests || true'
            sh 'cd ./${BUILD_ID} && mkdir root_results'
            sh 'cp -r ./${BUILD_ID}/API-Simple-mircoblog-app/allure-results ./${BUILD_ID}/root_results'
            sh 'rm -rf ./${BUILD_ID}/API-Simple-mircoblog-app'
        }

        sh 'cp -r ./${BUILD_ID}/root_results/allure-results ${BUILD_ID}'
        sh 'ls -las ${BUILD_ID}'

        withDockerContainer(args: '-u root', image: 'python:3.9') {
            sh 'rm -rf ./${BUILD_ID}/root_results'
        }
    }
    stage("Publish test report"){
        sh 'ls -las ${BUILD_ID}/allure-results'
        allure includeProperties: false, jdk: '', results: [[path: '${BUILD_ID}/allure-results']]
    }
    stage("Cleanup"){
        sh 'ls -las ${BUILD_ID}/allure-results'
        sh 'rm -rf ./${BUILD_ID}'
        sh 'ls -las .'
    }
}
