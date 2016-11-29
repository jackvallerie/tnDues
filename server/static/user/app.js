(function(){
        $("#get_all").click(function(){
                get_all_users();
        });


        function get_all_users() {
                $.get("http://localhost:5000/api/users",
                {

                },
                function(users, status){
                        if (status == "success") {
                                console.log(users);
                                display_users(users);
                        }
                        else {
                                console.log(data);
                        }
                });
        }


        function display_users(users) {
                var table = $("#user_list")
                for (var i = 0; i < users.length; i++){
                        user = users[i];
                        table.append("<td>" + user.first_name + "</td><td>" + user.last_name + "</td><td>" + user.email + "</td>");
                }
        }

}());
