import {
  login,
  register,
  watchUser,
  addJob,
  getUser,
  fileToDataUrl,
  updateUser,
  isLoggedIn,
  getFeedLength,
} from "./helpers.js";
import { renderNavBar } from "./main.js";
import { displayFeed, generateJobPost, update5post } from "./feed.js";

var pageIndex = 5;
var defaultImage =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIkAAACPCAYAAADOffjUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAC/rSURBVHgB7V0HeBNXtv4lSy6Se7dcccP0HjqmhV5CCKSwSUhvpO1mk01CNsvbbPZtGmnkJWSTTQ8ECD10ML1jejXuHfcmq79zRhIIM5ILZoOMf76L5JnRtHvmnP+Uewe4+eFLLYOaqa212Njo++AEkOEWRqiXB8LkgNRkQolRiqzKOmG5l5srIpUyKI16VEpkyKzWQKs34FbFLSUkAT6e0GoN6OItR1KID3r2GwhVx64wSVyQmXYWaXtTUFirQc8unZDUfyhkru4oKSnG6R2bkFt0CXtK1NAajKit10BPn7cKbgkhiY32hZenC6b2HQ5JfT2CO/dEl2Hj0KFrTyiUSmGbutpaXDy0C5UFOeh++1R4BwQJy02kZYpzs3BuzzYM3LkB9Wo1lqemwk1RiwNHynErQIKbH8xJUqnFoIWYMi4U0So9nnrjGIJCwnC9ePHxUYgL2o1587W4HhAnmZWenvUTbnK0eU3i4SZDWPCVv0uKi3D0yCEMHDIM+3bvRHhkFPQ6Pdxc5WADInORkSkxQKFQ4Mzpk4iLT0BgUAjysrOQ2LkLZDLzLfPxliE02AWFxWq0dUjRxjFyWCAmjKi9/HdNTQ02/rYaqYcOoLTkEry8vLFy+RJs27IJhQX5WLr4J/z1lRdRV1eLfbt2oIiWXTh7Gp/Ofwc7tm66vJ/ocCOefMALPkR+2zravCZZt6UI4WRi3FzNpsFoNCA0TAVVRCROHDtKQpCHrt16wMPDXdASg4clQxUeTtojGP0GDERwaBjyc3MxdtJUaIiwWnEx2wXzv6xAZfX1mRxnQJsXEqlUgrJKI8LMPBSx8Yn446t/Fb4/9fyfhM/etw286jdDkkcKn+MnTxM+4xOTrtmvRmMgbaPHrYA2bW5YQCaM9Me9U+pE12s09Th/9hTOnjqBioorngprm/zcbJw4mkqapkDwcBoiKd4Fc58Pgne7uXFucN8ePl6Lzole9JeROt/cCvJysXXzBiz+4VtcOH9O2LZjUmc8+tQziIzqgK++WIDt2zajvq4OYapwDB0xCndMn4HefftDIqXnymREcYkRi1bVoLqmHm0dt4QLPG1CCIb0kyKjMIq4hweqqmqIpOZdoyGUChcEBvgjO+cSGuoOX19f+PsHQCaXQ6/JRYBXLt549/oEpN0FvomQlqFFWIgrdPpsaCyWJziQ/7/6GZHLdDAZChESJMO1BqYStdWVwjcprT2S5Ubf2r4WYdwSQnLiTDk1tKOFaPNxknZcP5xGk3z11VcYOXIkWgpTXTVxkNZLykk9KOcjbdnt02g0uP322+Ht7acDsnCzw2mEJJwCXDExMWgp0mb2ha4wB62FmM/XwKNzP7QEarU5lE/BOxOcAO3mph2Nol1IbCChsLzE3R3tuBrtQkKQulHexs8fbjGJCLz3aUhcXSEPDEY7zLilyxetMOo0iHjja7iqYuHiGwiv4ZOQ/9Yc6EqK0Y52TSKYGK+BIyEPjoRc1QFShRdk/qHwSp4AF6Un2tEuJDDp9VCfOwlNxhmbZVqoz6TCqG37ZQBNQbu5IRgqy2DSaVG9czXxks6oTzsBY1WFsKwd7UJihsGA/H88D3loBBS9B6Ji9aJ2L8cG7UICzvybI7Haghxo12Sbl9XfGsm7pqBdSGxhvHXG0jQHt6SQlOkMkNA/Xxn9L7FfUlNnMEfNFS7OUHZz43DLCInWaML5Oi0u1BtwwKBHhSswRO+Cvl5uUHsApWU69Pd246IzyMnnO16txY56PUxKKe6UyRHlZq4xKdMaEODqglsJbVJItqSk4FBeCf4wfKCQGOQKtEyNDgtkdQjr6IoApQI9VUoU5OqxU+GKkho9smqBlHojemsMGOMtBxck1QS7Y+C4ECz4NgsT/Iw4qdZjX3Y9klWuSD55FlNamOBzNrQpIVmyfDm2ZhRgWHggvvrqY5zb8Bb++PIPSEpKwvyMGkgDXSCRekAqccXRUxrUayRISnBDQIAn+vaKouUS5P58Bq5SCbzIFMXGByK+QzD098sQF+8OSXY5NIfLKLuvwW3xsagnclty6RJc3dwQHNx2w/hOJSRGda3Q7CEqLBSXVizCqbwV6O2pQ5ivO3JOH4MXdCgxViFW6YZM0h6R4a7o1ikYJ8/WQC5T4tzFSuzaX4aBvUNRVqnFcqU7dMkd4C034cKFegzoG4Ws3HKkHtUhKrUelWSSlq5bjY1v/hWhoUHCQK4HH5iDPp07QqnwgJnCiPMYzhNBKoczwamEpHzlNyhbtMDu+rklSlzSl8FXp8NDd0uw8EsdpqbNQ6qO2IRGjV5dw3DkZD16dA7Btr2X4O3pjtp6CXp0VSFt7TlERYVghTET3cd0x6GVqZhGkdfjtTr8dC4CfqFK5J2rwmCFDCeSFDh9/msM7GoioapFWLAGr7+yDhO8guEHd/T2kiPUDm9xj0+C/6v/B2eCk2mSOujLSu2uf9pYQZ1cBQmZER5sV1pqgklbhkK1DuPHByMtU4M6tQm1agkiVb7omBACX28llpOA3DW5N0orDEgelIB6nQxdaurQOcgDSZ5y7DxZgC35njC6yrHdwxV3jItEYUklaZAaeHvpEa0yQhWiw8HDhUjNkqKzxhd6d3Eh0ZeXC0MynAltipMkyQzoWSPFkSrAhXgF8VFcrDPgvEwKo8ZEJiaIzEYh9p3WoEYNBPhrUVSsJ54iR6C/H4KCvLFszSpMHtcbiygbXJdfDAMRW01MKIYNiEZZRRX278vGp/88jSC9ESEkB/laI1YG6DF7NtCnlwQl7hLIL6BNoc15N0PIpT2RpkV+kQlRHaT48UgddPTgRib6kRaRYvqkRPwjcyCIwiI0/TeEhvjhjol96ZcuyMmrRcilMuz9IQUjpg6An68bNFXVSD+egWPfHkAvEsK/+7lDEaK46pjZ9Tqs31sJXa0Uw3M9EaJsWy5ymxISjmOkVKpRF6ODr48HHrjLB1/p6rBlSwW8f8vDq88FY+f+IugUlQguOIJZDw9AWlYlaupM0Ot1OHO+CEkR/phVU4L0JeuhpR16SUzoTgLVw5O8HYU75CLBN465uZJ5UR+Xoou/K9oanFpIpEpP4hzay9laDQXMCtRGXCAucvSUCWOHu+GJ+/3Je9GiU2Igdh8oxtMP9Uf0rlMI7xaBoku1UHgosXPvOWFekspqNcpK67GFgmh5GiPqVSHwjA1HRHwwArxl+GbZHiSUVSLQQkqryeSUkmiWx0mgNrmgk/Far8XFyxuG6io4M5xSSOTBocI4X5/hE6HJvgh9cR60RflwJVc0jJ7oKBVxg3J2Ql3g4e6K6EgFPDxccFvvKKip8wf0IX5RZSJt44uUPReRkVlMAkPmgjo9KiICZcm9MKJ/EuI6BEDpYYTRUAsDaSRFkALvfrQRvZN86RhuFB/RQq+tQ8bREiQclGFUwJXMsUen7tDkpCPwoT+SR/Y5ZEEhUJ86BmeEc2oSEw9p+A1SdyXpeh10RTnInHMncQ8TKGiKNOqLmMkuqKunSGtuHfILtZgwKgSXSEt4edWjijSGkrRQdl45Vq49iKGDuuG3lfMhlyshJRJrNGjI/JAnpa0RmsnoIuR4OsUHYfTwBKz+9y4EBrqi1iShWIoUT3u7EvG9moe4xnRE5L9+gtTTFz63z0TZks+dVkicrjJN6u4Gn/Ez4OJGQSsvX7j4BkEWqILPiAlwc5Figr874kn2T5zRUT7GQAGzKup8CdZtyUYQPem5eZUkLLUURHPB/P9bj7vuGIy5L99nCX3x/1KYJFIYSOC27jiOV+f9iINH0klzcTIQuGtSEiY/3BeFlM8ZSfsbF+hx2fxY4RYdD2XvwcK5SWg7F58AKHoOgkfnHnBGOGH5ogR1qXthrL8y54iOzI363Amhj93J9e1JuZfsDErO0b/OiZ6CaYqO9MTh48VwpQ4tLa3BvkMZqCGNkjy4E4xG0kbaeqRdzMCp02ewZu02PPrkP/HQk+/hu5+34c23l+HCxQJhf1KpCdMmxiFsShw+yKwRPUNDVTnqzx69all92iloc2/+0XpicDpzY6R8iUmnQe2RnXCN6EDBtWKBuOrLS2ilObVfR9wiNkiC9T+XQBnng/Ejg/DZN+lw95AjPbsalVU60iQyLPzwQZw8nY79hy7AjTTTT0tS4O/njQH9OgoxkReemojT57IQFuKFv7/3Gz57ZxKxHAOZOwPGDw/D4a1ZAll2I8HkQ0stjo++vBQSuRxlixfAK3kSavZtojS0moSnAvIQFZwNTslJWGuo334Biu59obtUCF1B7uVUCSfpZod7mbcj3/SrHeX4ODcfOurBvzzXG0P6x2P73gISGCXefn81CUkufOQuiHCTYLSvK855+OGpR25H6rEOGNw/lvgJda5eje8W78azr6zEvFcGwseLp8HSI5kzxD9nETk2oihMi6giObooZViZp8Gz330Olbsc6vPHULNzIwm3887S6LTElVF3/NA1y2zhQZm2fj6u+LVCh3vu6YBxw1XEN4BQCrdzUk9aWo6HIhRQKNwQLjOhq7sUxy9mYtHSbegQFYh1mw5RXkaBjqSNKipq4JtehLfe2IzBY6IQFyOHSiWDZoYPwoLUFJY3oLBIi8MnNThbSG6x1oAwMm1Vm1bC2dFmgmnMO9IoR1NF4dWuXq6CCWDkawyI66jE3ZNDyWOpx5m0Cpy5UI0lq87jMU+gSumPX+NG4MXbdNhDRPUubQHcVm1AFUkd/RTzqyV4792p0JOJ60iR1D4Udf35x9NYxS44/a2VGOARZsRTfzAI88BqdKTBiC7pfdBm0GbG3Syq0OOVsL7Y3akaSytriCNQIs9gxO4qLUYOUqKclp1Nu4RV6zOwZ38OhrkYSMu4QVpbhbBT67Fr71nc8+pkmCb1x/l6A/EaE07UGNC5Wyhli4H770qA+6SOyFIb8Ga8Nz6O9cKj5Pq+S3xFlUlkuIJIsxuEbQMCgVM1OrQVtBlNcqePC3LP7ECaiszG3Rr87+56cIXA6McViI4AikuqsXhVOdIvqhFAxPWFTr7YTzRhZ9wAuJsKMHyQivhMHcZPTETxAJXgAQ0OdoenQora2lpkZJdDQplh8rLxjE8fZBllmDN0L3JT6uERYYC/L2WdKYBXWQ0Eal0wNrDtzMrYJoSEtcaHGh+c6BaPR/vtR3Q4kPAHCaprScP8rEF2eBUOXSgDMox4U6Wg/IxScJVH0lPvVXYEX2ik5N0EYe+BC9i7Nx/dB3ZAnwQPlJSUYd3RAmg1WtTU1iN8fz4GUYIvqmAf/lVUh+IIGbrdrUWc0khkljLOWSZcPA+Mc1HAX952Bkc6lZB4xHejQNrd1yznBNtI4gE9y3KwcpMJd0+UIL/YBInUE7N6TYeXhwcS01YjPkaNCJs6jwpylb+VR8NLVo/DB3MgOZyPE56x2FNeiclJmSjIrsS5tEoK5esxNECOOuIpnD1eHTUInbsfIcEogRcJyMnzUsj9/FB6qYSIsQr97hgPH29xTSLzD6aEjnM9m051tp5DxwlNDIMvXsSbi35BTVkGUg6chZ/qIRh1WXj5oy+F6cCjLxy4ZqYjL/J+3tClw1smRelZI4IpgzvelI8cEjbjLj0CyEMZRC61jhK7yeQmGwKUOFmrQ2FxEboED8G+I8vM1fUBf8GyjHw81DMRz752JyIjYyjKa79E0TrTkbOgzXASlUqFaUmJCB/1OeLj44VgmZu7++W3SohBRgJgLTNUeJg/Y0lbxCrYVLiKbA/0Js+ptvIiFkoHQenVH3VSFWZNno6hlZVITk5GW0SbERKexHf69Om40WDHehjFXsbdOw7e3efBj8xMW0f7MM8WIjgoCB63gIAw2qfDakejuOmFpE+fPiY3NzdTcfGNn5pKShzGLToWNxocd+EXIeh0OqcoWXMGIanz8vI6u2HDBtwouHh6wnvUZPhMvBd+M56E19Ax8OjSEzcK+/btpRhMiSkxMfE4nAA3vZAsXLhQFx0dsWDlypXaffv24UbAUFMDr2ETEfI0EdHJDyD4ibnQ3aDaj7KyMrz//gfw8fFZvWTJkkI4AZyCk0yaNHWdt7f30tGjR2Pr1q1oTUjJKwqZMxdeyZMhkVPyhdxi16iOiHz3R8gCg9CaqKqqwpw5c3DgwIGSyMjIV+AkcAohmTdvnpHc24eDAwP/PXHixDqel3337t1s03G9MFJgq+izt1Gzcy0FxgzCrEfa/HTk/OUB6Esu4XrB3CMvLw/vvvsuEhISsHr16nMkIDMPHz58Fk4CpxlFRE+foaKycnVsbOzOrKws72+++SZix44dbp7EJ3jOeUcRTkbZkoUw1ojzRJ6K0zUiBjW718Ok16Fq0zKh0s1QYX9Iqe+k+yAPCocj5ObmknC8g2eeeRrr1q3PCgwMfKNv377P792716lerOK0U/gQoe2Wk5PzRkVFxZROnTq5vfzyy5g5c6bdCGtTXkDg4ukF1+h4qE+lCmYHJvvvB3D0AoILFy7g448/xqJFi0wajeZkWFjYJxQRXpKSklIBJ4TTz/M0a9asiC1btjxPwjIrKioq9KWXXpJw5NXf3/+q7W70Wyp4rpLU1FR8+umnWLFiRa1M5pIaHR3zflJSEhNUA5wYbWYysPHjx0ccO5b6cllZxczg4OCQV155Bffdd5/w7jzGxfv6Q5ubidYAj8GJ/mItPJL6XBaODz/8EKtWrdIrFB6H6PDvdevWjYWjTUwE65Qjm9988033ysrKDipVdGJQUEDwwPHj1WuWLi2uqqpev3jx4uUUrCojghhJneSv1WpATzQCu/YmTlIB/aUCYRbolkKuihJG5bn3G4Vt23fgxRdfxD/+8Q9tdnb2NuJLjz/44IN/W7Zs2akZM2a41NTUxASpVIkhQUEhcXFxBjKPtXBCOJUmId7hRZ3/aNeevR7t2bNvTHBomGtNTZXhwL7dVcdSj/ykCg39YPPmzcJErN27dw8mYXm0oKBgjqura9hTTz2F58j99K0qQOnPC1C9ezNMWk2Tj+0aEY3A+5+DS+8R2LTnAN555x0cO3as3tNTuYI0xwdBQUGpxDn0jz/+uE9Kyo6ZMR1inxk6YmSH4JAwhVZbrz9xLLVq355dKxXu7vMp3tNOXFsb9BTGx8bG3xeiUv1p+sz7vP2IbxQVFQovh2Z178evIaF4x/IlizTp584uonVfTJky5SC5znriKEoSrJkF+flPS6TSnvSkyx5++GEkBXmj7Pv5qN61EYbKctHjSuSuxDt6wn/GY1An9sXqtevw0UcfGc+fP19AZmwdEeZ/kWCkkWaTkvYIp3OYmZiY9MKYiZMjYmJiUVZeCqPBILjBHh4K+FJCcONva/QH9+1bezHz4oc+SuXuw4cP3/TFsDe9kISEdFcOHtZp96zZj/RQKpTQG/RITOoMP/+Ay9sYqCOOHj4gzLJYXV1N3w/pzpw6ueL0iaNf33bbbTu///772meffdZt7dq1sy5dunQ//WQgkVs3FpaeqgDUbVyEWtIsPPicIXHzgLLvEPhPm42y4Dh89+NP+OWXX5CRkZHl7u7+A8U5fjxy5IigDQYPHtxRrVY/PGDIsPsGDhkW4ePrB3d3D0SRiQsIsp1sz4TUQwegI+3lQsK3dsWvpl0p229PTT24BTc5bnpOUltbpBwzbuLzMR06+Hbt1QuxcYnCU8nIzszAxQvnoQqPgCoiEr7+fjDoDVAqFC59+w/oEhYeMfX48WPd3Fzll+rqgvNSU7cdHDVq1HISqqMHDx4MWbp0aXRGcZkkccosxEy6GzIFvxwpAKEv/hPyiQ9g4Yr1eObZZynGsa6YyOpC8p6eSEtLW04mrKRPn8FRgYG+r3bv3ffjx+e8MCYuoaM3JSLRpVtPxMTGQ6FUIic7C4cP7EckCYxU6oIwVQRCwsKRnZVBWsVfsn/PrtWFhfmncZPDaepJFJ5KeHp6X7Wsrq4Of37haXz53SISngQoFJ7o1KUbkjp3RcbFNAqDV3q98fd/3pV6+ND0tSuX7yHzMI80yzbq9GUDBw78jfIowygnNO+HH364bcyY2yWvvz4XIbcH4q2vvsZ//jOdtVJuUEDAJxSs++706dOFRDwlpDm6VNXUPDdg8G0zJ99xl29NbTXkMjkJRw8ovbwEbZabk4XPF3yE/v0HITgklCLD2svxG/50dXWDM8Fpi464M86eOYVu3XqhsqISGelpWL18GcZOmIyOnTojNj5BaOkXzyMyKlry2t/+PpiEZePWTetT4+PjP6M4yjKKfHJqeUNycnK//fv3vzRs2LAx9DfxXPmZkJDg75944okFzGvGjBmjdHFx6ROmUv2xa4/ed0+cOs2llpKCWp0GQ0eMJi0hFUzesdTDWL50MfQkFAOHDscvP36H4aPGCFyEhVju6pyzIDmtkGxatwbnzpxGeFQkdu/YJkRI09MuCB2ybs1K1KvrMW3G3YJ54paXk01cJgk9e/fplXb+/Jc7t299qXPnzgvc3HxXbd++/SDt8m7SMgNLS0ujSGh++/rrr6sDAgLcaJsJMjePh+5/+MlxcQnx7gqFQjAdfQcMolSAudML8nKxZdMGXDh3Rnjn78Qp0zB0+Ejs2rYF4RERWLPiVzzy5DPwdfWHM8JphYRcS0y+404cPLAP8fEdsWLZIvzp1bkCX8lMv4hff/lZEJLCgnyhM8Mjo0AcBfm5OegQa4B/QEBHMhfzU7ZufLKmrnRteFjYQvJU9tKu906bNk1JybjpW7Ztn/Pgo08MjomNkzMZDQlTIaZDHFzIZHBy8eC+PYJADh81VjjOk8/+kYREjU/efwfdevbCpGnTsWfnDsy4ZxZzEDgrnFZIevbpK3wy/9i7ewfqauvgQd7Pu2/PI6UiJdsvh56CZjtTtuLrLz7DohVrBVc0IipaaOVlpUR6z7kMHzm684TJ0zrv2LZ5Vnp6+i9ka7IvpKU//Jc330ry8fGRsVeSRDwnKDhUMCscnNtErnBxUQEdsxYuLjIsXfwjtKRBVv76C56c8wJCVSqcPXUSAwYOwYBBQ4RtnBlOXwjNHTeY7H//gYPxwzdfkZofRU97LEouFQuvnddo6pHQsSPKSkvx9KP34535n5EX5M88BX2JWNbV1uDA3t1IHjFKlTxy9AtFhQXEabogizhOfGJH0kDRl4+Vevggtm/djMyMdNx7/2xyz0NB3gk09TxPfT02r/+NuIkef37tTbQlOJ2QVFdXIS87ExSWpw4xCmNrvMmrYC0y+9EnhW2YQMYnJFBwbTHCyESEqcKxecM6PP/n15CVmY4FH72HT7/8FgX5eYL7PHz0WEETHDm4X+h4BZmsMROngMNIxRS0y0xPR3dyv3cSx/D29sHQ5BECD3rosaewbctGYZs/v/ZXjB0/STh+bU018ZQ8OsdyElItM2F40Tm6035ZizkbnEZIqkgodu/YCpPBJEQyy8vLBXXPLzcKj4xAdEwHcnsvQEXco0evPoJLeoA4Q3xCIs6cPkUBtoOYfs99+J+5r2DuvLeFaO1bb7yGf330KSUB/YQ3TVBA7Kpjsge1ZsUyrCKvadiIUUgir+n0qRPo3LUbVtPy7SQ0zDVYqzCZrawoF86BR+ix91OYnw92kdn8eXt7o+9tA7Bj6yZhuZeP88xNcdMLCVfLl5aWGDnKeurYMSxbsqhAq675MLew8MDRQ4cye/XqFViv0/WLj094ZMTosX04Ert960ZBQwyydPqEyVMxfvIdRDT3CkMwI6KiiMfswv2PPCYICE/0q9VqhfgFE1Kj0QA3N3fiEi64694/CNXtcSRsa0hYZs56EMuIFD/17IsCH/KhLDMLx+7t2xBIEVY6V6xdtbwk+2LaQorjbDh+/HhuYmKiksL4PTavW/v4bYOHDhk+cpTk1InjJIT6OjgBnCF3IyFBGCeTy2dXVlSsHTt27OJPPvlELDMn6dGjxxhvP78Xx4ybPGrwsGGyYuIXUZRDiUtMErhLYUEeli76EV279wJ30jMv/En4IZPM77/5NzqT9tFQLoi9I37qp9x5l7B+z87tQnvmhZfIZHgIGobLBZi/nDl1DDIXOWsP47LFP2UcOXxwQUxU1PfkKZU0PEHO8axfv74XxVQer6tTlw0ZMvivXOiNmxxt7uVylKJ3pRzLaHel57PTZ96TTFl6D5lcRmanI8IodM9mgeMp4ZGRwlyujItp5/Hr4p8xbOQogb/s2LYVf5j9yOV9VldV4sSxoxg0NFkgwzlZWYJZ4TB8cVGRkYjv6d07diyMjY3+ZdWqVUVoY2hzL5Oj8LkhPz//wtQpk5euXrE8pbAwz01dp04gziFoltKSEjITXYQknBXMH9gbYvIbToJUWnIJCeTZWF/iyKaH8y/pJEwsHBVlZcijeMvK5UsO/Lrop/816LQv7d+/N+XcuXNOWS/SGNr8ayrJNEj69x/a3ctH8XCX7j2fHjN+oow5CLutyRQyZ95h2U74NAsGf5dcXn6WyCoHy4JDw4isbjLt3pGyqyAn54OQkJBtmzdvrkQbxy31LlPO3KrV5XN69O33yP2zH/NX15kf/F79+pOLenXykOMraefOkrudBU8fb5w7e6Zu+S8/76itrn577ty5e2bOnOnUdavNwS35wtsJEyaEFhYWPtClR68nxk2YEuvj5ytkauPiOlIm1xPnz56miGwJhe6DsH3LxuotGzas0uu1848QIDoZaNvGLf1W5K5du8YFBAVNjYqOeYYSdrE9e/WlxKBaCNgRUVWnbNq4lLyQr3r16rbHGbyQG4Vb+9XZFpBH5JOTkzMpMDh0FukJt8qK0v3V1dW/TJ069SSXCqAd7WhHO9rRjna0ox3taMfND/ZuQqnVU+MZaHnsKscBuJybXxpTZ2mtAWu0qsqyfyU1HmXPL3fgNxxKLU1vOZ+bCXxeXH8YYfm0Xgu7xTyyiycyyUPr3aubCiwkq6j1p8aZVWsUkWPV3JF3UNuL1sE8ao/CLIh83D3UZlv+ftiynjsjxbL8RsQl3oD5GlkIY6i9Tq3awfYdqfE85XwfomAWbL4vtqEDFnIO3XLWN4Xaj9R24Orzf4xaIszCZB1E7mHZ5/cw34uWgDOUc6mVWfbLQvwJtZbO5cXX9SrM18TywHOQfsor+KJMdlpHtB5eb7Dv73DlZs9usG4Bbkyty4YGx7E3802k5fxMLWw8FJBHClqvjwVNa2fbf6LliBfZ74toOVjoztjs6xQ1GT+59qRObWmthYYTuJTiSoi74bqnqP0VrR/ss53qiK9NTFtx3eJumDvZCtY+adT+Rm0stT7UelObQO1/qTWc+ITn+fyG2uOWv9dQy4Q4eqHl18nHbyjok69jf0w9Ymz+Zi0nBBOfh7iE88yAIWg9zG6w/zds1t0hcnx+Qp5D6wrK1zb7F5sQbQbMvML2PPiVnX+B2TzYQxi1j2C+ofwbVtfv4+o56T6F+H3OwNUd0xxsgXi/haFleNJmP5zdvjyp7f0QP/kL1ALQepgJ85Nr3f9zNutG2jkH3v4PaD18iKs7xxb8FJU3OD5zlxdg3yzZggWCBZ8FZDvM/MUW3SzrGl4jLxuD5oOFtgri920cmg92HpbZ7GMbLA8oX5i92eP4BFozHW5s8HeFg3VWMC/5ktp9aB3YXo/tS335ZvwPNd8G26fArCGaQqKt2oPfzPgxzGTWFieopYr8jo99G5oPNotedtbdjeaD5yNNtvn7V1joAAuJvcne2Ga3ppDwU2krDE2dMpsl/AtqA3H9sD2mrbvKZnWiyPbr0LzSAN7ny9R22Vm/3M5yHmnWXKI+wcG6EWi+mWZNZ7UcbOp/sa5gIbHnAvKGrZkB5X3ZContk2xVcfbArHsRtc5oPdjGYqJhNjcNcQ7NB5tpe3WuSyCuuXmO8ubwP35whjhYz9fTFc2D7XiSw7C5BhaSGjs/Yj+5OU9Rc1HX4FiNaS2OKWxCy0keGhzD1hywyys28XFLCaA9sGu8Q2Q5X1sHNB3coRGW7xzHEvNC70HzMMXm+8+2K/jG8I0TG6LQ2uamIewVDfMIf3tzafI73Dei5YJSb+f4SjvbT0PTSGtTwdp0hchyNg1D0TTwtszReEoD7h/mUpki281C001YHLVOlu/lDc+RhYRNgBgx4xO4kZrEngY7Se1Oatl21ifAzMKjcH2wffrYHRa7Vva62LtqzcAeez65Isub6uFwFPR2y/cCagdgQzJtwCanB5qGETbfrzI1DEdzyxth3+toCUwNvtvjOyw8/H75Z2E/F8KBLHZnFWg5bLUKC6QYN2MNwx4Lx5Ja6zVZrCV3iywfAPveii264IoZ/A3mkPw6y2dDjELTYEuC1+JK6kCAIyHhDmpNIeH9WQXDEQexLuec0l0QN4UMNgUcvm/p3FK25oZfBpBpZzsWDo6q8usx+CV/1/tWaL6nG3HtvWUy2pQnn++J1XNZYvncD/Hzn4HGvRye/W+w5Tt7f9e8BuS/+ZYKk53vDImddfyEcLDPnqA8QG0hmm4ObDWTrblj4bUm/8TA+2cPZCnMQTjWLhxTYJexJfcwBeJezthGfseazWpqOKG43fKdz/83ke05qZgAx2DNZJ1hhx+Wkw03+L1eZcLqzLZDWBtYRxM2NDHMP56GeDyHz58J2gdomqq2fXobmjvOr3yKxsk6u6p/hLmjuZPepTYe4i60PaTDnEhrCBYSR6MqmVxaO521iC2XXIxrz51LGkbDMTjXY33IfoCI9fi9hEQsLmLVJg1JNJ/0t9TehDi55JvKCcG/oHmoFTkOlyuwaWnqnPD8FLLAsDewHmaexCajKYEssbc7sZfhyO3mSCp3KN+H1Q3Wccb2vMhv2DzZm9GPTZw1PsKaba3YRv9NIZE5OF5jN5WfkM+ove1g3y/BXK/SVIh5dOz+sdnhGMNRNB3cCSwcTHA52srnGtnIb8RcYeY/3Rz8xuoBZcLs1TTEZpFlHM0NhDj4hT2Jlu88n2yG2Eb/TSGxVp8x2LOwVfdNmdGFt+cCm/l21nNHcc7kMVwf+Cnl8Dl7UGzK+MZXN+P3HB3mbCq/hHEa7D/Fx3Btp0gsvxFDErXulu/s8op5MxwEa6ht2Qzb83LG4oqZXgE7IY//ppBIYF9jNGd2Ay5e+g/EXWj2PJifWNWyIzRmUviG/QTz09vfclwWmKa+e5aThWzjeQ4Le9e3TWQZB9XEsu/3Wj51lvMS61BOI4hpgztFlnGQcKrlO2vqpXAADu9W49p0M/OA1qzl4BO1lgpwEMhWBT5oc9w3m7Avlv7vYb8yjEnuTJHf2dZLPIjmg4WQi4SegTlFoEXjVWpswuwFysTqaFjLjmywHQvZHst61lD23H7ur4Ui+yzFta57NK6UGhyGAzjSJB5o3flLWA3LHByrOWCh5nqUbXbWs/liXpCM1gVHaTndz/EZ7mAmfVz+6aiUgDUKV6iJmR2Ob+Q1WMYC0DDjzWami+U7hwXshQS4w9kUNfRy2MVtKKisHa2mxl52WoAjIWES1Zp5C1vWbhtYY7QkcspPKMdJ9ttZzyqb61S748aAvSN+UTHHcTjIluFgWxZWMfLIsQ6xQnMObtlqC3ax2Z1lzeWwQ2GOVovFYBrW5Iy3fLLg/woHsOZuxIYw+KPl0Uwx2GY5+QbbcgJPtAycA2FBOWVnPed3OH7QCzcOVneUo5v23hHLAhIsspw1kJiQ8FNufSkx94GVeHI98kk4BgueWPU918tYHQR++CdZvnO8xpGAXx7nIsbemaso0XroYvOdmbltgq2lQsLg2MAMiMcIGOwVMCnrixsLtuvvO1jvbmc5u8wNA4j8gPa0fOe6EKs25MCivcSoLcQ0A/flIMt33rdVs/EIAocF71LLBmKMnSU5GK0DtstxNn+zT27Lzm2jpS3JjfDTwNlaezeQC3rZ04jAjcUmB+vsDTjjc78gstzKIVgDWL2dFWgarAXSDWH1ZqxahLnNKjQCFhKWYrGnsKW1l2LgijLbLGrDaKOtkLTUxHEdCntQZXbW8xii13BjYa8UlIXX3nmxFhcrd+RIKT8wLCTcF2xaD6BpyIe4yeECaX5grS4xk+YTaATWoiN7Nr0lVddi4KfCqm75hjUsCG6t6ZHZ2/kz7JcYNObSX2/cKMbOcs7VOJqAj01VQw+JiT6n8K0lm2I1I44gRnDZOnAFmpUfclKwyTNGssaogbjPHo3rAwuA7agwznHYdgZ3XIrN+i9wfWBXk4dB8Lk7il88iKvB53S9wzfesXOsBY38jhN3RSK/s963lgy7iIH4EI5Tlk9+kJpabyKA4xfrIH6B/8b1BdX4yTbY7K9hOpyZ9j6b9f/B9YPP919onpBwbIJH6bWUt7A5qxQ5Dtv9xjqYBfSAg3NlzhKI5oHvwRkH++R1zQ49DMe1o9esF/kCWgYONqlt9rVSZBu2u0dttlmE1gEHAjlqLPY0NRQS7oDduJK3ae7NY1f7oJ3jbGji/t6D/Q7lfFVLHtT5DvbZmHYTBUvzR3Z2yMLzDzRdmlkzse27ZLMPJlPxItsyab1gs11TGXxTwDUea+BYSPj4X9osZ63HwtzUIBy7qEfsHOMSmj60YbydfXCIYiJahuGw/5C0mG9yvOInOztlYsVFNnNgtqFiIXb2xdmccP6gwua3mbh6XIctOCaQa7PtZrQuOE5yHNdez8Mwk2mObehE1nOVFpcNcHynIaHlv1mI/gaz8IvdL77+SWg6WFjFeBR7njFoGZioinEdNovXVYbJJ8uqTwPxizdaDsJjSHbC/KQyS2Z1nYFrCTBHCB0FspjF247B3Y/WB3sIeQ3O63nLOg4w8TXYe+I4Ccb2m2MgbIqYu7HbWAH7qpw7lpN0zTUR+0T29TVankNjYRYbVL4WrQSOyvHNszco2VHjJzMT5ukjGpPYGFz9JLdk1FxTwNNF2Arw8zbruDO5Wp2vVywj3pTGZoor4Vn7BKFleBvXPpDN0UZieBrXnutDzdmBo5oLJpPMK7jiimscmKFz5JJvACebbLOarHW4A3jaA46BcPiYR6qVoXGwd8PEmNU2PzF+ls/WHhjGsQi+Oa9bztd2bAnfOH6KueCHK7XYZHKMgs1qCMSfZKuWYQ3FSTXWMk29ZntgPsYPDA/xYC3Antb1zjTFIYe3YNbyvE+OfC9rzg6aow75AMw5WDO4Wj6ZtTOp5ZvO9pSfwtac+OZGgM/bGrhyNNaZHyCO8XBqgoNPTNr5fvH1cZaVhYPNbg2uaKh2tKMd7WhHO9rRjnbcILRmoXNLwKPZedgCE2Gua2B2L0YmOWrJEUmOp/zbZjl7W5xSPwvxuggOlnHSztPmbyaYnJVl1t/YUAmu42DPi/NADWtVeOgGZ1B/cvB79qbYWzPaHJ9jSsdFtuXr43gO19qss1nOyVeOuXCcxmHBclsER275xn8Os3BwOaO9UDh7JByU4w4eZLOcI7tcMBVv53csHBzwYw+Mo8UsSOyisyfGAjcFjmEdSfAfXFvIzPUa3zby+/WWY3PnWssE7cU9OIXApYccRoi2LGMPa5vlGlpzkkOnAMcdOCrJOQ/WZhzl5cCbo4Ijrk7nJ5IDXnzzeIQcd/aDDn7DLjon2DJxZdI8duU5AswdxhrF0QxDViFh7fY+rta8nD74FI7BsRMePpJk+dt2zLMYXoH5QeCIN18jx2tYmEfiFgTfKA7rc2i7WxN/w53LBcfcYcNhfopZdTuq6Gf1zqqbBaLhzIp/g1noHNWQsJBY543n475ss47V/3twDB7UbSskjYE130XLMTlnxOUDbOpccYuCx81Yh1awuWnKdFA8HRYHsvjGs2pObGR7R0JiHRj1uoPfs5DkWLblDmPN9YRlHQvJ3+AYLCRqy7ZselirNTYPG3MTDk6ypmWBaWmIv9Xwe80qwGBVPRtmrsHcgDuzMUHh0D1zGLbfrFXOo+Wwqv2mkPdMmCvyWUDZ7FgLipsSZbV2+BlLa2x4qTWRyFNM8JDVS/id8XsKCat6niuUp5r8E8w2uCkleta8Q3NG/YuBzRx38hkH2/D98bKcG4954UFYzBEWoOlmkjUJvzmCXwzAnlJpI9uzZrUWRh/DTYDfS0j4KeZ6DjYB7OGwKuZ8SlPeF9MaU3SxN8Rmg+s9tznYzs3SrIlQTgKymeQamBA0Pii9pSGGmyoPdCNeF9IU8E3myWI4TsJjaZk8crKsKXUO1lLAppA5vj7WBJyou9tyDK5FnQ1zjIMF1VHWlrPdLrjaI2FTwO47axN3OAYTUaXlOOyqsxvLQrkRjZ83ozVHULYYrTkgvDlglcpeCRcfczCMK9N4xqDUJvyW60lZA3Gc4lQj2/JNZs+CywLYxve0LGM3mmdGOt3I79nNZqLJPKHQZjmbAe5I1oK7HPyeyyyYYLOgMulmLsWp/0w4BhNyLpXY0OC4tyT45rHa/j25UUvBwtZa03be1Ph//GDW9H4xrAIAAAAASUVORK5CYII=";
let intervalId = null;
let running = false;

window.addEventListener("hashchange", function () {
  renderNavBar();
  route();
});

window.addEventListener("DOMContentLoaded", function (ev) {
  renderNavBar();
  route();
});
function changeHash(hash) {
  window.location.hash = hash;
}

function clearDOMNode(id) {
  const node = document.getElementById(id);
  node.textContent = "";
}

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
function validatePassword(password, confirmPassword) {
  if (password == "" || confirmPassword == "" || password != confirmPassword) {
    return false;
  }
  return true;
}

// poll for updating posts
export function startPolling() {
  if (!running) {

    intervalId = setInterval(function () {
      update5post();
    }, 500);
    running = true;
  }
}

export function stopPolling() {
  if (running) {

    clearInterval(intervalId);
    intervalId = null;
    running = false;
  }
}

// route user to specific URL and render given page
function route() {
  var hash = window.location.hash;

  const loginContainer = document.createElement("div");
  loginContainer.setAttribute("class", "container pb-5");

  const col = document.createElement("col");
  col.setAttribute("class", "p-5 m-auto rounded-lg");

  const formContainer = document.createElement("div");
  formContainer.setAttribute("class", "container bg-light p-3 rounded ");
  formContainer.style = "max-width: 700px";

  const form = document.createElement("form");

  var m1 = document.createElement("div");
  m1.setAttribute("class", "mb-3");
  var m2 = document.createElement("div");
  m2.setAttribute("class", "mb-3");

  var m3 = document.createElement("div");
  m3.setAttribute("class", "mt-5");

  var m4 = document.createElement("div");
  m2.setAttribute("class", "mb-3");

  var m4 = document.createElement("div");
  m2.setAttribute("class", "mb-3");

  var loginEmailLabel = document.createElement("label");
  loginEmailLabel.setAttribute("class", "form-label");
  loginEmailLabel.innerText = "Email address";

  var loginEmailInput = document.createElement("input");
  loginEmailInput.setAttribute("class", "form-control");
  loginEmailInput.setAttribute("type", "email");
  loginEmailInput.setAttribute("placeholder", "Enter Email");
  loginEmailInput.setAttribute("id", "email");

  var loginPasswordLabel = document.createElement("label");
  loginPasswordLabel.setAttribute("class", "form-label");
  loginPasswordLabel.innerText = "Password";

  var loginPasswordInput = document.createElement("input");
  loginPasswordInput.setAttribute("class", "form-control mb-1");
  loginPasswordInput.setAttribute("type", "password");
  loginPasswordInput.setAttribute("placeholder", "Password");
  loginPasswordInput.setAttribute("id", "password");

  var confirmPasswordInput = document.createElement("input");
  confirmPasswordInput.setAttribute("class", "form-control mb-3");
  confirmPasswordInput.setAttribute("type", "password");
  confirmPasswordInput.setAttribute("placeholder", "Confirm Password");
  confirmPasswordInput.setAttribute("id", "Confirm-Password");

  var nameInputLabel = document.createElement("label");
  nameInputLabel.setAttribute("class", "form-label");
  nameInputLabel.innerText = "Name";

  var nameInput = document.createElement("input");
  nameInput.setAttribute("class", "form-control");
  nameInput.setAttribute("type", "name");
  nameInput.setAttribute("placeholder", "Enter name");
  nameInput.setAttribute("id", "name");

  var forgotPasswordLink = document.createElement("a");
  forgotPasswordLink.setAttribute("class", "link-dark");
  forgotPasswordLink.innerText = "Forgot your password?";

  var formSubmit = document.createElement("button");
  formSubmit.setAttribute("class", "btn btn-primary w-100");

  var signUpLinkDiv = document.createElement("div");
  signUpLinkDiv.setAttribute("class", "text-center mb-5 mt-1");
  signUpLinkDiv.innerText = "New to LurkForWork? ";

  var signUpLink = document.createElement("a");
  signUpLink.setAttribute("class", "btn p-0 pb-1");
  signUpLink.innerText = "Join Us!";
  signUpLink.addEventListener("click", () => changeHash("#join"));

  var welcomeContainer = document.createElement("div");
  welcomeContainer.setAttribute("class", "container mt-5 mb-5");

  var welcomeRow = document.createElement("div");
  welcomeRow.setAttribute("class", "row");

  var welcomeContainer1 = document.createElement("div");
  welcomeContainer1.setAttribute("class", "col-lg-7 text-center my-auto");

  var unswLogo = document.createElement("img");
  unswLogo.setAttribute("class", "img-fluid mb-4");
  unswLogo.src = "img/unsw_logo.png";
  unswLogo.alt = "unsw_logo";

  // Welcome Page Components
  var welcomeMessage = document.createElement("h2");
  welcomeMessage.innerText = "Welcome to your professional community";

  var welcomeButtonDiv = document.createElement("div");
  welcomeButtonDiv.setAttribute("class", "btn-group mt-4 mb-5");

  var welcomeJoinButton = document.createElement("button");
  welcomeJoinButton.setAttribute("class", "btn btn-primary");
  welcomeJoinButton.innerText = "Join";
  welcomeJoinButton.addEventListener("click", () => changeHash("#join"));

  var welcomeSignInButton = document.createElement("button");
  welcomeSignInButton.setAttribute("class", "btn btn-primary");
  welcomeSignInButton.innerText = "Sign in";
  welcomeSignInButton.addEventListener("click", () => changeHash("#signin"));

  var splashImgDiv = document.createElement("div");
  splashImgDiv.setAttribute("class", "col-lg-5");

  var splashImg = document.createElement("img");
  splashImg.setAttribute("class", "img-fluid");
  splashImg.src = "img/splash_art.png";
  splashImg.alt = "splash_art";

  // clear the main node and grab it to add content to
  clearDOMNode("main");
  var main = document.getElementById("main");

  if (hash.length == 0) {
    hash = "#welcome";
  }

  var hashElements = hash.split("=");

  // switch case to determine  page to be rendered
  switch (hashElements[0]) {
    case "#welcome":
      main.appendChild(welcomeContainer);
      welcomeContainer.appendChild(welcomeRow);
      welcomeRow.appendChild(welcomeContainer1);
      welcomeContainer1.appendChild(unswLogo);
      welcomeContainer1.appendChild(welcomeMessage);
      welcomeContainer1.appendChild(welcomeButtonDiv);
      welcomeButtonDiv.appendChild(welcomeJoinButton);
      welcomeButtonDiv.appendChild(welcomeSignInButton);

      welcomeRow.appendChild(splashImgDiv);
      splashImgDiv.appendChild(splashImg);
      break;
    case "#join":
      if (isLoggedIn() == true) {
        changeHash("#home");
        break;
      }
      main.appendChild(m3);

      var messageDiv = document.createElement("div");
      messageDiv.setAttribute("class", "text-center");

      var registerMessage = document.createElement("h3");
      registerMessage.innerText = "Make the most of your professional life";
      messageDiv.appendChild(registerMessage);
      main.appendChild(messageDiv);

      signUpLinkDiv.appendChild(signUpLink);
      formContainer.appendChild(form);

      form.appendChild(m1);
      m1.appendChild(nameInputLabel);
      m1.appendChild(nameInput);

      form.appendChild(m2);
      m2.appendChild(loginEmailLabel);
      m2.appendChild(loginEmailInput);

      form.appendChild(m4);
      m4.appendChild(loginPasswordLabel);
      m4.appendChild(loginPasswordInput);
      m4.appendChild(confirmPasswordInput);

      formSubmit.innerText = "Join";
      form.appendChild(formSubmit);

      loginContainer.appendChild(formContainer);
      main.appendChild(loginContainer);
      formSubmit.addEventListener("click", function (event) {
        event.preventDefault();
        //Resets red borders in case for correct format
        loginEmailLabel.style.color = "";
        loginEmailInput.style.border = "";
        loginEmailLabel.innerText = "Email address";

        loginPasswordLabel.style.color = "";
        loginPasswordInput.style.border = "";
        loginPasswordLabel.innerText = "Password";

        confirmPasswordInput.style.border = "";

        nameInputLabel.style.color = "";
        nameInput.style.border = "";
        nameInputLabel.innerText = "Name";

        //gets form inputs
        var email = document.getElementById("email").value;
        var password = document.getElementById("password").value;
        var confirmPassword = document.getElementById("Confirm-Password").value;
        var displayName = document.getElementById("name").value;
        var validStatus = true;
        //Checks that all values are valid, highlights all that are incorrect and sets valid status as false
        if (validateEmail(email) == false) {
          loginEmailLabel.style.color = "red";
          loginEmailLabel.innerText = "Please enter valid email";
          loginEmailInput.style.border = "1px solid red";
          validStatus = false;
        }
        if (validatePassword(password, password) == false) {
          loginPasswordLabel.style.color = "red";
          loginPasswordLabel.innerText = "You cannot have a blank password";
          loginPasswordInput.style.border = "1px solid red";
          validStatus = false;
        } else if (validatePassword(password, confirmPassword) == false) {
          loginPasswordLabel.style.color = "red";
          loginPasswordLabel.innerText = "Passwords are not matching";
          confirmPasswordInput.style.border = "1px solid red";
          validStatus = false;
        }
        if (validatePassword(displayName, displayName) == false) {
          nameInputLabel.style.color = "red";
          nameInputLabel.innerText = "Name cannot be blank";
          nameInput.style.border = "1px solid red";
          validStatus = false;
        }
        if (validStatus == true) {
          register(email, password, displayName).then((data) => {
            if (data["error"] == undefined) {
              updateUser(undefined, undefined, undefined, defaultImage);
              changeHash("#home");
            } else {
              renderError(data["error"]);
            }
          });
        }
      });

      break;
    case "#signin":
      if (isLoggedIn() == true) {
        changeHash("#home");
        break;
      }
      var signIn = document.createElement("h3");
      signIn.setAttribute("class", "mb-0");
      signIn.innerText = "Sign in";
      var signInSub = document.createElement("p");
      signInSub.innerText = "Stay updated on your professional world";
      signInSub.setAttribute("class", "fw-light mb-1");

      main.appendChild(m3);
      form.appendChild(signIn);
      form.appendChild(signInSub);
      form.appendChild(m1);
      m1.appendChild(loginEmailLabel);
      m1.appendChild(loginEmailInput);

      form.appendChild(m2);
      m2.appendChild(loginPasswordLabel);
      m2.appendChild(loginPasswordInput);
      m2.appendChild(forgotPasswordLink);

      formSubmit.innerText = "Sign in";
      form.appendChild(formSubmit);
      formContainer.appendChild(form);
      loginContainer.appendChild(formContainer);

      signUpLinkDiv.appendChild(signUpLink);
      loginContainer.appendChild(signUpLinkDiv);
      main.appendChild(loginContainer);

      formSubmit.addEventListener("click", function (event) {
        event.preventDefault();
        //Resets red borders in case for correct format
        loginEmailInput.style.border = "";
        loginEmailLabel.style.color = "";
        loginEmailLabel.innerText = "Email address";

        loginPasswordLabel.style.color = "";
        loginPasswordInput.style.border = "";
        loginPasswordLabel.innerText = "Password";

        var email = document.getElementById("email").value;
        var password = document.getElementById("password").value;
        var validStatus = true;
        // Ensure format of inputted email and password is correct
        if (validateEmail(email) == false) {
          loginEmailLabel.style.color = "red";
          loginEmailLabel.innerText = "Please enter valid email";
          loginEmailInput.style.border = "1px solid red";
          validStatus = false;
        }
        if (validatePassword(password, password) == false) {
          loginPasswordLabel.style.color = "red";
          loginPasswordLabel.innerText = "Please enter valid password";
          loginPasswordInput.style.border = "1px solid red";
          validStatus = false;
        }
        if (validStatus == true) {
          login(email, password).then((data) => {
            if (data["error"] == undefined) {
              changeHash("#home");
            } else {
              renderError(data["error"]);
            }
          });
        }
      });

      break;
    case "#home":
      if (isLoggedIn() != true) {
        changeHash("#welcome");
        break;
      }
      pageIndex = 5;
      renderHomePage();
      setTimeout(function () {
        startPolling();
      }, 2000);

      break;

    case "#me":
      if (isLoggedIn() != true) {
        changeHash("#welcome");
        break;
      }
      stopPolling();
      renderMePage(hashElements[1]);
      break;
  }
}

// render profile page
function renderMePage(user) {
  var renderUser;
  if (user == undefined || localStorage.getItem("currentUser") == user) {
    renderUser = localStorage.getItem("currentUser");
  } else {
    renderUser = user;
  }
  const meTemplate = document.getElementById("me");
  const meClone = meTemplate.content.cloneNode(true);

  document.getElementById("main").appendChild(meClone);

  var watchBtnTest = document.getElementById("my-watchees");
  getUser(renderUser)
    .then((data) => {
      if (data["error"] == undefined) {
        var watchButton = document.getElementById("watch-me");
        var userImg = document.getElementById("my-img");
        var userName = document.getElementById("my-name");
        var myWatchees = document.getElementById("span-watchees");

        userImg.src = data.image;
        userName.innerText = data.name;
        myWatchees.innerText = data.watcheeUserIds.length;
        watchBtnTest.addEventListener("click", () =>
          renderListModal("watch", data.watcheeUserIds)
        );

        if (
          data.watcheeUserIds.includes(
            Number(localStorage.getItem("currentUser"))
          )
        ) {
          watchButton.innerText = "Unwatch";
          watchButton.setAttribute("class", "btn btn-danger mb-3 rounded-pill");
        } else {
          watchButton.innerText = "Watch";
          watchButton.setAttribute("class", "btn btn-dark mb-3 rounded-pill");
        }

        watchButton.addEventListener("click", function (event) {
          event.preventDefault();
          if (watchButton.innerText == "Watch") {
            watchUser(data.email, true);
            watchButton.innerText = "Unwatch";
            watchButton.setAttribute(
              "class",
              "btn btn-danger mb-3 rounded-pill"
            );
          } else if (watchButton.innerText == "Unwatch") {
            watchUser(data.email, false);
            watchButton.innerText = "Watch";
            watchButton.setAttribute("class", "btn btn-dark mb-3 rounded-pill");
          }
          location.reload();
        });
      } else {
        renderError(error);
      }
    })
    .catch((error) => {
      renderError(error);
    });

  if (renderUser == localStorage.getItem("currentUser")) {
    var editButton = document.getElementById("edit-button");
    editButton.addEventListener("click", function (event) {
      event.preventDefault();
      var newName = document.getElementById("new-name");
      var newEmail = document.getElementById("new-email");
      var newPassword = document.getElementById("new-password");
      var confirmPassword = document.getElementById("confirm-new-password");
      var newImage = document.getElementById("new-image");

      var emailLabel = document.getElementById("new-email-label");
      var passwordLabel = document.getElementById("new-password-label");
      var imageLabel = document.getElementById("profile-pic-label");

      //Reset labels
      emailLabel.innerText = "Email address";
      emailLabel.style.color = "";
      newEmail.style.color = "";
      newEmail.style.border = "";
      confirmPassword.style.color = "";
      confirmPassword.style.border = "";
      newImage.style.border = "";
      newImage.style.color = "";
      imageLabel.innerText = "Profile picture";
      imageLabel.style.color = "";
      //set valid flag to true
      var validStatus = true;

      if (!validateEmail(newEmail.value) && newEmail.value != "") {
        newEmail.style.color = "red";
        newEmail.style.border = "1px solid red";
        emailLabel.innerText = "Please enter a valid email";
        emailLabel.style.color = "red";
        validStatus = false;
      }

      if (
        !validatePassword(newPassword.value, newPassword.value) &&
        newPassword.value != ""
      ) {
        newPassword.style.color = "red";
        newPassword.style.border = "1px solid red";
        passwordLabel.innerText = "Password cannot be empty";
        passwordLabel.style.color = "red";
        validStatus = false;
      } else if (
        !validatePassword(newPassword.value, confirmPassword.value) &&
        confirmPassword.value != ""
      ) {
        newPassword.style.color = "red";
        newPassword.style.border = "1px solid red";
        passwordLabel.innerText = "Passwords must match";
        passwordLabel.style.color = "red";

        confirmPassword.style.color = "red";
        confirmPassword.style.border = "1px solid red";
        validStatus = false;
      }

      if (validStatus == true) {
        var email = newEmail.value;
        var password = newPassword.value;
        var name = newName.value;
        var img;

        if (email == "") {
          email = undefined;
        }
        if (password == "") {
          password = undefined;
        }
        if (name == "") {
          name = undefined;
        }
        img = undefined;
        if (newImage.files[0] != undefined) {
          try {
            fileToDataUrl(newImage.files[0]).then((base64str) => {
              updateUser(email, password, name, base64str);
              location.reload();
            });
          } catch (error) {
            newImage.style.border = "1px solid red";
            imageLabel.innerText =
              "provided file is not a png, jpg or jpeg image.";
            imageLabel.style.color = "red";
          }
        } else {
          updateUser(email, password, name, img);
          location.reload();
        }
      }
    })
  } else {
    document.getElementById("edit-profile-button-user").style.display = "none";
  }

  displayFeed(renderUser, "profile");
}
//might need to chagne this
export function isValidDate(dateStr) {
  // check if the date string is in the format dd/mm/yyyy
  const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
  if (!regex.test(dateStr)) {
    return false;
  }

  // parse the date components from the string
  const [day, month, year] = dateStr.split("/").map(Number);

  // check if the date is valid using the Date constructor
  const dateObj = new Date(year, month - 1, day);
  if (isNaN(dateObj.getTime())) {
    return false;
  }

  // check if the date is not in the past
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  if (dateObj < today) {
    return false;
  }

  // the date is valid
  return true;
}

// Render Home Page with feed
function renderHomePage() {
  const postWatchTemplate = document.getElementById("postWatch");
  const postWatchClone = postWatchTemplate.content.cloneNode(true);
  document.getElementById("main").appendChild(postWatchClone);

  //Sends post requeust to add a new job when button is pressed
  var postButton = document.getElementById("post-new-job");
  postButton.addEventListener("click", function (event) {
    event.preventDefault();
    var jobTitle = document.getElementById("addJobPost-title");
    var jobDate = document.getElementById("addJobPost-date");
    var jobDesc = document.getElementById("addJobPost-description");
    var jobImg = document.getElementById("addJobPost-img");
    var validStatus = true;
    //resets invalid inputs
    jobTitle.style.color = "";
    jobTitle.style.border = "";
    document.getElementById("new-role-title").innerText = "Role";
    document.getElementById("new-role-title").style.color = "";

    jobDate.style.color = "";
    jobDate.style.border = "";
    document.getElementById("new-job-date").innerText = "Start date";
    document.getElementById("new-job-date").style.color = "";

    jobDesc.style.color = "";
    jobDesc.style.border = "";
    document.getElementById("new-job-about").innerText = "About";
    document.getElementById("new-job-about").style.color = "";

    document.getElementById("form-image-add").style.color = "";
    document.getElementById("form-image-add").innerText = "Image";
    document.getElementById("addJobPost-img").style.border = "";

    //Check if inputs are valid
    if (jobTitle.value == "") {
      jobTitle.style.color = "red";
      jobTitle.style.border = "1px solid red";
      document.getElementById("new-role-title").innerText =
        "Job must have a title";
      document.getElementById("new-role-title").style.color = "red";
      validStatus = false;
    }
    if (jobDate.value == "" || !isValidDate(jobDate.value)) {
      jobDate.style.color = "red";
      jobDate.style.border = "1px solid red";
      document.getElementById("new-job-date").innerText =
        "Invalid Starting date";
      document.getElementById("new-job-date").style.color = "red";
      validStatus = false;
    }

    if (jobDesc.value == "") {
      jobDesc.style.color = "red";
      jobDesc.style.border = "1px solid red";
      document.getElementById("new-job-about").innerText =
        "Please add a description";
      document.getElementById("new-job-about").style.color = "red";
      validStatus = false;
    }
    if (jobImg.files[0] != undefined) {
      try {
        fileToDataUrl(jobImg.files[0]).then((base64str) => {
          if (validStatus == true) {
            addJob(
              jobTitle.value,
              base64str,
              jobDate.value,
              jobDesc.value
            ).then((data) => {
              if (data["error"] == undefined) {
                renderError(data["error"]);
              }
            });
            location.reload();
          }
        });
      } catch (error) {
        document.getElementById("form-image-add").style.color = "red";
        document.getElementById("form-image-add").innerText =
          "Provided file is not a png, jpg or jpeg image";
        document.getElementById("addJobPost-img").style.border =
          "1px solid red";
      }
    } else {
      //default image
      if (validStatus == true) {
        addJob(jobTitle.value, defaultImage, jobDate.value, jobDesc.value);
        location.reload();
      }
    }
  });

  //Gets the current user's image and replace it next to the post button
  getUser(localStorage.getItem("currentUser"))
    .then((data) => {
      if (data["error"] == undefined) {
        document.getElementById("user-post-job").src = data.image;
      } else {
        renderError(data["error"]);
      }
    })
    .catch((error) => {
      document.getElementById("user-post-job").src = "";
    });

  //watch user
  var watchInput = document.getElementById("watch-input");
  watchInput.addEventListener("keypress", function (event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      var email = watchInput.value;
      if (email != "") {
        watchUser(email, true);
      }
      watchInput.value = "";
    }
  });

  //generate inital 5 jobs.
  displayFeed(0, "home");
  window.addEventListener("scroll", function (event) {
    if (
      window.innerHeight + window.scrollY >=
      document.documentElement.scrollHeight
    ) {
      displayFeed(pageIndex, "home");
      pageIndex = pageIndex + 5;
    }
  });
}

export function pollNotifications() {
  var feedCount = 0;
  var notifCount = 0;
  var start = 0;
  var end = 0;

  setInterval(function () {
    if (isLoggedIn()) {
      getFeedLength();

      if (localStorage.getItem("feedLength") != null) {
        feedCount = localStorage.getItem("feedLength");
      }

      var notificationData = JSON.parse(localStorage.getItem(`feedData`));

      if (notifCount == feedCount) {
        return;
      } else {
        start = notifCount;
        end = notifCount + 1;

        notifCount = notifCount + 1;
      }

      appendNotifications(notificationData, start, end);
    }
  }, 5000);
}

// append Notification to Offcanvas
function appendNotifications(notificationData, start, end) {
  var notificationOffcanvas = document.getElementById("notificationsOffcanvas");

  for (let i = start; i < end; i++) {
    getUser(notificationData[i].creatorId).then((data) => {
      let postTime = formatTime(notificationData[i].createdAt);
      let headContent =
        data.name + ' posted "' + notificationData[i].title + '" ';

      let notificationList = notificationOffcanvas.querySelectorAll("div");
      notificationList[1].appendChild(
        addNotification(headContent, postTime, "../img/new_post_icon.png", i)
      );
    });
  }
}

function formatTime(backendTime) {
  var postTime;
  var postTimetoDate = Date.parse(backendTime);
  var currentTime = new Date().getTime();
  var timePast = Math.floor((currentTime - postTimetoDate) / 1000);
  var hoursPassed = Math.floor(timePast / 3600);
  var minutesPassed = Math.floor((timePast % 3600) / 60);

  if (timePast < 60) {
    postTime = "Posted less than a minute ago";
  } else if (hoursPassed < 24) {
    postTime = `Posted ${hoursPassed} hours and ${minutesPassed} minutes ago`;
  } else {
    var day = backendTime.substring(8, 10);
    var month = backendTime.substring(5, 7);
    var year = backendTime.substring(0, 4);
    postTime = `Posted ${day}/${month}/${year}`;
  }

  return postTime;
}

// generate a notifation to be added
function addNotification(name, post, img, id) {
  const notificationTemplate = document.querySelector("#notification");
  const notificationClone = notificationTemplate.content.cloneNode(true);

  let notificationImg = notificationClone.querySelectorAll("img");
  notificationImg[0].src = img;

  let notificationP = notificationClone.querySelectorAll("p");

  notificationP[0].innerText = name;
  notificationP[1].innerText = post;

  return notificationClone;
}

// render Watch or Like Modal
export function renderListModal(type, id) {
  let userListModal = document.getElementById("user-list-modal");
  let userList = userListModal.querySelectorAll("#user-list");
  // clear list
  userList[0].innerText = "";

  if (type == "watch") {
    let icon = userListModal.querySelector("#modal-icon");
    icon.src = "../img/watch_icon.png";

    let modalLabel = userListModal.querySelector("#user-list-modal-label");
    modalLabel.innerText = "Watchers";
    for (let i = 0; i < id.length; i++) {
      getUser(id[i]).then((data) => {
        userList[0].appendChild(
          addUser(data.name, data.email, data.image, id[i])
        );
      });
    }
  } else if (type == "likes") {
    const userIdsArray = id.map((obj) => obj.userId);

    let icon = userListModal.querySelector("#modal-icon");
    icon.src = "../img/like_icon.png";

    let modalLabel = userListModal.querySelector("#user-list-modal-label");
    modalLabel.innerText = "Likes";
    for (let i = 0; i < id.length; i++) {
      getUser(userIdsArray[i]).then((data) => {
        userList[0].appendChild(
          addUser(data.name, data.email, data.image, userIdsArray[i])
        );
      });
    }
  }

  let myModal = new bootstrap.Modal(
    document.getElementById("user-list-modal"),
    {}
  );
  myModal.show();
}

export function renderError(error) {
  const errorModal = document.querySelector("#error-modal");
  const errorModalModalClone = errorModal.content.cloneNode(true);
  errorModalModalClone.querySelector("#errorContent").innerText = error;

  document.getElementById("main").appendChild(errorModalModalClone);

  let myModal = new bootstrap.Modal(document.getElementById("errorModal"), {});
  myModal.show();
}

function addUser(name, email, img, id) {
  const userItemTemplate = document.querySelector("#user-li");

  const userItemClone = userItemTemplate.content.cloneNode(true);
  let userItemImg = userItemClone.querySelectorAll("img");
  userItemImg[0].src = img;

  let userItemP = userItemClone.querySelectorAll("p");
  userItemP[0].innerText = name;
  userItemP[0].addEventListener("click", () => changeHash(`#me=${id}`));
  userItemP[1].innerText = email;

  return userItemClone;
}

export { changeHash };
