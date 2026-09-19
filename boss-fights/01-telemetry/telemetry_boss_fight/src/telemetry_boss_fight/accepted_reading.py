# accepted reading

# | field | meaning | units |
# | --- | --- | --- |
# | `timestamp` | when the reading was taken | ISO 8601, UTC |
# | `robot_id` | which robot | our identifier, e.g. `amr-01` |
# | `velocity` | ground speed, signed | metres per second |
# | `battery` | charge remaining | percent |
# | `temperature` | motor controller temperature | degrees Celsius |

# | field | valid range | why this range |
# | --- | --- | --- |
# | velocity | `-2.0` to `2.0` m/s | the drive firmware hard-caps at 2.0. Reverse is the same magnitude — the robots back into docking stations. |
# | battery | `0` to `100` % | it's a percentage. |
# | temperature | `-40` to `150` °C | the rated range of the motor controller's sensor. Outside it, the number means nothing. |


