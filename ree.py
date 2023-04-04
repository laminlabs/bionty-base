import lamindb as ln
import lnschema_core as lns

ln.setup.load("lukas-bionty-test")

stmt = (
    ln.select(ln.File).join(ln.Run).join(ln.Transform).join(lns.User, handle="zethson")
)

print(stmt.df())
