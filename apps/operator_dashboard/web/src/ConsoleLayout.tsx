// Adapted from TencentDB Agent Memory ConsoleLayout.tsx (MIT); see UPSTREAM.md.
// Retains Tea Layout/Body/Sider/Menu/Content composition; removes backend state.
import { useState, type ReactNode } from "react";
import { Layout, Menu } from "tea-component";

const { Body, Sider, Content } = Layout;
export function ConsoleLayout({
  children,
  page,
  onPage,
}: {
  children: ReactNode;
  page: string;
  onPage: (page: string) => void;
}) {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <div className="operator-shell">
      <header className="operator-header">
        <strong>Devtools</strong>
        <span>Operator / read-only pilot</span>
      </header>
      <Layout>
        <Body>
          <Sider>
            <nav aria-label="Operator views">
              <Menu
                collapsable
                collapsed={collapsed}
                onCollapsedChange={setCollapsed}
              >
                <Menu.Item
                  title="Work Portfolio"
                  selected={page === "portfolio"}
                  onClick={() => onPage("portfolio")}
                />
                <Menu.Item
                  title="Worker Activity"
                  selected={page === "activity"}
                  onClick={() => onPage("activity")}
                />
              </Menu>
            </nav>
          </Sider>
          <Content>
            <Content.Body>
              <main>{children}</main>
            </Content.Body>
          </Content>
        </Body>
      </Layout>
      <footer>
        MemoryPanel components © 2026 Tencent ·{" "}
        <a href="/UPSTREAM-LICENSE.txt">MIT license</a> · Devtools adaptation ·
        No execution authority
      </footer>
    </div>
  );
}
