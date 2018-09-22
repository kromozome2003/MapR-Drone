maprcli stream topic delete -path /demos/drone/drone1 -topic frames
maprcli stream topic delete -path /demos/drone/drone1 -topic resized
maprcli stream topic delete -path /demos/drone/drone1 -topic analyzed
maprcli stream topic create -path /demos/drone/drone1 -topic frames
maprcli stream topic create -path /demos/drone/drone1 -topic resized
maprcli stream topic create -path /demos/drone/drone1 -topic analyzed
