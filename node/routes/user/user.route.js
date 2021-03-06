/*
 * @Author: ghost 
 * @Date: 2018-04-10 10:59:10 
 * @Last Modified by: aroop.ghosh@tarento.com
 * @Last Modified time: 2018-06-29 10:18:27
 */
var userController = require('../../controllers/users');


module.exports = function (router) {
    router.route('/list-users')
        .get(userController.listUsers);

    router.route('/list-roles')
        .get(userController.listRoles);

    router.route('/create-user')
        .post(userController.createUser);

    router.route('/v1/user/signup-user')
        .post(userController.signUpUser);

    router.route('/v1/user/forgot-user-password')
        .post(userController.forgotPassword);

    router.route('/set-user-password')
        .post(userController.setPassword);

    router.route('/update-user-status')
        .post(userController.updateUserStatus);

    router.route('/v1/user/activate-account')
        .post(userController.activateAccount);
}