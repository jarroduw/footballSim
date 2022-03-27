# README for football_sim

This is a very simple object-oriented simulator design for football games. It depends on very minimal stats at a team-level to make predictions.

The simulator execution is set up in the "run_sim.py" script. The configuration of the statistics to use for configuring scenarios is specified as a yaml file, including:

```yaml
team_name: <team_name>
pass_pct: <probability of calling a pass in a given play>
pass_stats:
    yds: <average yds per game passing>
    sd: <sd yds per game passing>
run_stats:
    yds: <average yds per game rushing>
    sd: <sd yds per game rushing>
punt_stats:
    yds: <average yds per game punting>
    sd: <sd yds per game punting>
```

For purposes of studying a given matchup, calculate stats as averages and standard deviations for each of the categories, using per-game as the measure of standard deviation.
